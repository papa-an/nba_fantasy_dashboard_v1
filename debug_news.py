import requests
from bs4 import BeautifulSoup

URL = "https://www.nbcsports.com/fantasy/basketball/player-news"

def debug_feed_structure():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to find the main news container. 
        # Often these are in 'ul' or 'div' with class containing 'News' or 'List'
        # Let's just find the first text matching "Cam Thomas" (from our previous read) and print its parents
        
        target = soup.find(string=lambda t: t and "Cam Thomas" in t)
        if target:
            parent = target.find_parent('div')
            # Go up a few levels to find the "Card" container
            for i in range(5):
                if parent:
                    print(f"\n--- Parent Level {i} ---")
                    print(f"Tag: {parent.name}")
                    print(f"Classes: {parent.get('class')}")
                    # print(parent.prettify()[:500]) # Preview content
                    parent = parent.parent
        else:
            print("Could not find specific test string 'Cam Thomas'. Dumping first 20 div classes found:")
            divs = soup.find_all('div', limit=20)
            for div in divs:
                print(div.get('class'))
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_feed_structure()
