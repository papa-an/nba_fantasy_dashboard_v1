from src.data import espn_connector
import pprint

def inspect_settings_dict():
    league = espn_connector.get_league_connection()
    if not league:
        return

    print("--- League Settings Dict Keys ---")
    pprint.pprint(list(league.settings.__dict__.keys()))
    
    # Check if there is a 'schedule' attribute in settings
    if hasattr(league.settings, 'schedule'):
        print("\n--- Schedule Settings ---")
        pprint.pprint(league.settings.schedule)

if __name__ == "__main__":
    inspect_settings_dict()
