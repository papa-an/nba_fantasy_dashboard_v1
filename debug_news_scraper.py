import requests
from bs4 import BeautifulSoup

URL = "https://www.nbcsports.com/fantasy/basketball/player-news"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    print(f"Fetching {URL}...")
    response = requests.get(URL, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check for the old selector
        old_items = soup.find_all('div', class_='PlayerNewsPost')
        print(f"Found {len(old_items)} items with old selector 'div.PlayerNewsPost'")
        
        if len(old_items) > 0:
            print("\n--- Saving First Item Structure to debug_item.html ---")
            with open("debug_item.html", "w", encoding="utf-8") as f:
                f.write(old_items[0].prettify())
        
        # If 0, let's look for common tags to see structure
        if len(old_items) == 0:

            print("\n--- Inspecting Page Structure ---")
            # Look for likely candidates for news items (divs with 'news' or 'player' in class)
            candidates = soup.find_all('div', class_=lambda x: x and ('News' in x or 'Player' in x))
            distinct_classes = set()
            for c in candidates:
                if c.get('class'):
                    distinct_classes.add(" ".join(c.get('class')))
            
            print("Potentially relevant classes found:")
            for c in list(distinct_classes)[:20]:
                print(f" - {c}")

            # Also save raw html to inspect if needed (truncated)
            with open("news_debug_dump.html", "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            print("\nSaved full HTML to news_debug_dump.html")

except Exception as e:
    print(f"Error: {e}")
