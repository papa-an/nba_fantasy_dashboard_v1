import requests
from bs4 import BeautifulSoup
import datetime
from app.src.utils.team_mapping import get_full_team_name

URL = "https://www.nbcsports.com/fantasy/basketball/player-news"

# Simple in-memory cache
_news_cache = []
_last_fetch = None
CACHE_DURATION = datetime.timedelta(minutes=10)

def fetch_player_news(limit=15):
    """
    Scrapes the latest NBA player news from NBC Sports (Rotoworld).
    Returns a list of dictionaries.
    """
    global _news_cache, _last_fetch
    
    now = datetime.datetime.now()
    if _last_fetch and (now - _last_fetch < CACHE_DURATION):
        print("DEBUG: Returning cached news")
        return _news_cache[:limit]

    news_items = []
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # The main list of news items
        news_list = soup.find('ul', class_='PlayerNewsModuleList-items')
        
        if not news_list:
            print("Could not find news list on source website. Structure may have changed.")
            return []
            
        items = news_list.find_all('li', class_='PlayerNewsModuleList-item')
        
        for item in items[:limit]:
            try:
                # Headline usually contains player name + short summary
                headline_div = item.find('div', class_='PlayerNewsPost-headline')
                headline_text = headline_div.get_text(strip=True) if headline_div else "No Headline"
                
                # Extract all player names from links in headline
                player_names = []
                if headline_div:
                    player_links = headline_div.find_all('a')
                    for link in player_links:
                        name = link.get_text(strip=True)
                        if name and len(name) > 2:  # Skip empty or very short links
                            player_names.append(name)
                
                # Format player names
                if len(player_names) > 1:
                    # Multiple players: "Player1; Player2"
                    player_name = "; ".join(player_names)
                elif len(player_names) == 1:
                    player_name = player_names[0]
                else:
                    # Fallback: try to extract full name from headline
                    # Typically news starts with "FirstName LastName did..."
                    # Extract first 2-3 capitalized words
                    words = headline_text.split()
                    
                    # Find consecutive capitalized words at the start
                    capitalized = []
                    for word in words:
                        # Check if word is capitalized and not a common article/preposition
                        if word and len(word) > 1 and word[0].isupper():
                            # Remove punctuation from end
                            clean_word = word.rstrip(',:;.!?')
                            if clean_word and clean_word.lower() not in ['the', 'a', 'an', 'in', 'on', 'at']:
                                capitalized.append(clean_word)
                        else:
                            break  # Stop at first non-capitalized word
                    
                    # Use first 2 words as name (typically FirstName LastName)
                    if len(capitalized) >= 2:
                        player_name = " ".join(capitalized[:2])
                    elif len(capitalized) == 1:
                        player_name = capitalized[0]
                    else:
                        player_name = "Unknown Player"
                
                # Analysis/Report content
                # Everything in 'PlayerNewsPost-content' that isn't the headline?
                # Actually, based on structure, 'PlayerNewsPost-content' wraps everything.
                # Let's look for specific analysis class if it exists, otherwise generic text.
                
                # Based on typical Rotoworld structure:
                # .PlayerNewsPost-analysis usually holds the expert take
                analysis_div = item.find('div', class_='PlayerNewsPost-analysis')
                report_text = analysis_div.get_text(strip=True) if analysis_div else ""
                
                # If analysis is empty, might be just a 'report'
                if not report_text:
                    # Sometimes simple news only has 'PlayerNewsPost-story'
                    story_div = item.find('div', class_='PlayerNewsPost-story')
                    if story_div:
                        report_text = story_div.get_text(strip=True)

                # Date/Time
                date_div = item.find('div', class_='PlayerNewsPost-date')
                date_text = date_div.get_text(strip=True) if date_div else "Recent"

                # Team info
                team_div = item.find('div', class_='PlayerNewsPost-team-abbr')
                team_abbr = team_div.get_text(strip=True) if team_div else ""
                team_full_name = get_full_team_name(team_abbr) if team_abbr else ""

                news_items.append({
                    "player": player_name,
                    "team": team_full_name,
                    "headline": headline_text,
                    "report": report_text,
                    "date": date_text
                })
                
            except Exception as e:
                # Skip individual bad items but continue
                continue
                
    except Exception as e:
        print(f"Failed to fetch news: {e}")
        return []
        
    if news_items:
        _news_cache = news_items
        _last_fetch = now
        
    return news_items
