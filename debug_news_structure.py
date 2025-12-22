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
    
    # Just inspect the first item
    if items:
        first_item = items[0]
        
        print("=== First News Item Structure ===")
        
        # Get headline
        headline_div = first_item.find('div', class_='PlayerNewsPost-headline')
        if headline_div:
            print(f"\nHeadline div: {headline_div}")
            print(f"\nHeadline text: {headline_div.get_text(strip=True)}")
            
            # Find all links in headline
            links = headline_div.find_all('a')
            print(f"\nNumber of links in headline: {len(links)}")
            for i, link in enumerate(links):
                print(f"Link {i+1}: {link.get_text(strip=True)}")
        
        # Get team info
        team_div = first_item.find('div', class_='PlayerNewsPost-team-abbr')
        if team_div:
            print(f"\nTeam: {team_div.get_text(strip=True)}")
        
        # Get player meta
        meta = first_item.find('div', class_='PlayerNewsPost-meta')
        if meta:
            print(f"\nMeta info: {meta.get_text(strip=True)}")
