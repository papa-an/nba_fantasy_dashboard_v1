from src.data import espn_connector
import datetime

def inspect_matchup_objects():
    """
    Deep dive into Matchup objects to find period mapping
    """
    league = espn_connector.get_league_connection()
    if not league:
        return
    
    # Pick first team
    team = league.teams[3]  # North Bay Mamba (index 3 based on earlier output)
    print(f"Team: {team.team_name}")
    print(f"\nSchedule ({len(team.schedule)} matchups):\n")
    
    for idx, matchup in enumerate(team.schedule):
        # Get attributes of the matchup object
        print(f"Matchup {idx + 1}:")
        print(f"  Type: {type(matchup)}")
        print(f"  Attributes: {[attr for attr in dir(matchup) if not attr.startswith('_')][:10]}")
        
        # Try to access home/away teams
        if hasattr(matchup, 'home_team'):
            print(f"  Home: {matchup.home_team.team_name if matchup.home_team else 'BYE'}")
        if hasattr(matchup, 'away_team'):
            print(f"  Away: {matchup.away_team.team_name if matchup.away_team else 'BYE'}")
        
        # Check for matchup period
        if hasattr(matchup, 'matchup_period'):
            print(f"  Period: {matchup.matchup_period}")
        
        print()
        
        if idx >= 3:  # Just show first few
            break

if __name__ == "__main__":
    inspect_matchup_objects()
