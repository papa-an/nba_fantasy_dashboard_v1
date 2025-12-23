from fastapi import APIRouter, HTTPException
import requests
from bs4 import BeautifulSoup
import datetime
import re

router = APIRouter()

URL = "https://www.nbcsports.com/fantasy/basketball/player-news"

# Simple in-memory cache
_news_cache = []
_last_fetch = None
CACHE_DURATION = datetime.timedelta(minutes=10)

def get_full_team_name(abbr):
    # Basic mapping to ensure no dependency on legacy files
    teams = {
        'ATL': 'Atlanta Hawks', 'BOS': 'Boston Celtics', 'BKN': 'Brooklyn Nets', 'CHA': 'Charlotte Hornets',
        'CHI': 'Chicago Bulls', 'CLE': 'Cleveland Cavaliers', 'DAL': 'Dallas Mavericks', 'DEN': 'Denver Nuggets',
        'DET': 'Detroit Pistons', 'GSW': 'Golden State Warriors', 'HOU': 'Houston Rockets', 'IND': 'Indiana Pacers',
        'LAC': 'Los Angeles Clippers', 'LAL': 'Los Angeles Lakers', 'MEM': 'Memphis Grizzlies', 'MIA': 'Miami Heat',
        'MIL': 'Milwaukee Bucks', 'MIN': 'Minnesota Timberwolves', 'NO': 'New Orleans Pelicans', 'NOP': 'New Orleans Pelicans',
        'NYK': 'New York Knicks', 'OKC': 'Oklahoma City Thunder', 'ORL': 'Orlando Magic', 'PHI': 'Philadelphia 76ers',
        'PHX': 'Phoenix Suns', 'PHO': 'Phoenix Suns', 'POR': 'Portland Trail Blazers', 'SAC': 'Sacramento Kings',
        'SAS': 'San Antonio Spurs', 'TOR': 'Toronto Raptors', 'UTA': 'Utah Jazz', 'WAS': 'Washington Wizards'
    }
    return teams.get(abbr.upper(), abbr)

def fetch_player_news(limit=20):
    global _news_cache, _last_fetch
    
    now = datetime.datetime.now()
    if _last_fetch and (now - _last_fetch < CACHE_DURATION):
        return _news_cache[:limit]

    news_items = []
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(URL, headers=headers, timeout=10)
        
        if response.status_code != 200:
             # Fallback if site is down
            return []
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # NOTE: NBC Sports structure changes often. 
        # Looking for the list items that contain news.
        # This selector targets the 2024-2025 structure
        items = soup.find_all('div', class_='PlayerNewsPost')
        
        if not items:
             # Try fallback older selector
            items = soup.find_all('li', class_='PlayerNewsModuleList-item')

        for item in items[:limit]:
            try:
                # 1. Headline / Player Name
                headline_div = item.find('div', class_='PlayerNewsPost-headline')
                
                # Extract player name (usually in a span or anchor)
                player_name = "Unknown Player"
                name_tag = headline_div.find('span', class_='PlayerNewsPost-name') if headline_div else None
                if name_tag:
                    player_name = name_tag.get_text(strip=True)
                
                # Extract Team
                team_abbr = ""
                team_tag = headline_div.find('span', class_='PlayerNewsPost-team-abbr') if headline_div else None
                if team_tag:
                    team_abbr = team_tag.get_text(strip=True)
                
                # 2. Content / Analysis
                analysis_div = item.find('div', class_='PlayerNewsPost-analysis')
                analysis_text = analysis_div.get_text(strip=True) if analysis_div else ""
                
                # 3. Timestamp
                time_div = item.find('div', class_='PlayerNewsPost-timestamp')
                time_str = time_div.get_text(strip=True) if time_div else "Recently"
                
                news_items.append({
                    "player": player_name,
                    "team": get_full_team_name(team_abbr),
                    "team_abbr": team_abbr,
                    "headline": f"{player_name} ({team_abbr})", # Construct a headline
                    "analysis": analysis_text,
                    "time": time_str,
                    "source": "NBC Sports"
                })
                
            except Exception as inner_e:
                continue

        _news_cache = news_items
        _last_fetch = now
        return news_items

    except Exception as e:
        print(f"Scraping error: {e}")
        return []

@router.get("/")
async def get_news():
    """Returns the latest aggregated player news."""
    return fetch_player_news()
