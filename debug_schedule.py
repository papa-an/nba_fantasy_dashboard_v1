from src.data import espn_connector

def debug_schedule_info():
    league = espn_connector.get_league_connection()
    if not league:
        return

    print("\n--- League Attributes ---")
    # print(dir(league))
    
    # Try different naming conventions
    current_period = getattr(league, 'currentMatchupPeriod', None)
    if not current_period:
        current_period = getattr(league, 'scoringPeriodId', 'Unknown')
    
    print(f"Current Period: {current_period}")
    
    if current_period != 'Unknown':
        try:
            box_scores = league.box_scores(matchup_period=current_period)
            if box_scores:
                matchup = box_scores[0]
                print(f"Matchup found: {matchup.home_team.team_name} vs {matchup.away_team.team_name}")
                
                # Check player for schedule info
                player = matchup.home_team.roster[0]
                print(f"Player: {player.name}, ProTeam: {player.proTeam}, Schedulev: {getattr(player, 'schedule', 'None')}")
        except Exception as e:
            print(f"Error fetching box scores: {e}")

if __name__ == "__main__":
    debug_schedule_info()
