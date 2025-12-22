import requests
from bs4 import BeautifulSoup

URL = "https://www.nbcsports.com/fantasy/basketball/player-news"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

response = requests.get(URL, headers=headers, timeout=10)
soup = BeautifulSoup(response.content, 'html.parser')

news_list = soup.find('ul', class_='PlayerNewsModuleList-items')
if news_list:
    items = news_list.find_all('li', class_='PlayerNewsModuleList-item')
    
    if items:
        first_item = items[0]
        
        print("=== Inspecting First News Item ===\n")
        
        # Get headline
        headline_div = first_item.find('div', class_='PlayerNewsPost-headline')
        if headline_div:
            print(f"Full Headline: {headline_div.get_text(strip=True)}\n")
            
            # All links
            links = headline_div.find_all('a')
            print(f"Number of player links: {len(links)}")
            for i, link in enumerate(links):
                print(f"  Link {i+1} text: '{link.get_text(strip=True)}'")
                print(f"  Link {i+1} href: {link.get('href', 'No href')}")
        
        # Team abbreviation
        team_abbr = first_item.find('div', class_='PlayerNewsPost-team-abbr')
        if team_abbr:
            print(f"\nTeam Abbreviation: {team_abbr.get_text(strip=True)}")
        
        # Check for full team name
        team_name = first_item.find('div', class_='PlayerNewsPost-team-name')
        if team_name:
            print(f"Team Full Name: {team_name.get_text(strip=True)}")
        
        # Check the meta section
        meta = first_item.find('div', class_='PlayerNewsPost-meta')
        if meta:
            print(f"\nMeta content: {meta.get_text(strip=True)}")
            
        # Look for any element with "team" in class name
        all_divs = first_item.find_all('div')
        team_related = [d for d in all_divs if 'team' in d.get('class', [''])[0].lower()]
        print(f"\n=== All team-related divs ===")
        for div in team_related:
            print(f"Class: {div.get('class')}, Text: {div.get_text(strip=True)}")
