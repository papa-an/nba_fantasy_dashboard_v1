from src.data import espn_connector

def debug_matchup_dates():
    league = espn_connector.get_league_connection()
    if not league:
        return

    print(f"Current Matchup Period: {league.currentMatchupPeriod}")
    
    # Inspect settings for schedule info
    if hasattr(league, 'settings'):
        print("\n--- League Settings ---")
        # specific attributes that might hold date info
        print(f"Matchup Periods: {getattr(league.settings, 'matchup_periods', 'Not Found')}")
        
        # Sometimes it's a dictionary mapping period_id -> date info
        # Let's inspect the keys of settings to be sure
        # print(dir(league.settings))

    # Let's verify what box_scores for next period return
    next_period = league.currentMatchupPeriod + 1
    print(f"\nFetching Box Scores for Period {next_period}...")
    try:
        box_scores = league.box_scores(matchup_period=next_period)
        if box_scores:
            print("Success! Found box scores.")
            # Do box scores have date attributes?
            print(f"Box Score Attributes: {dir(box_scores[0])}")
    except Exception as e:
        print(f"Error fetching next period: {e}")

if __name__ == "__main__":
    debug_matchup_dates()
