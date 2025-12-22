from src.data import espn_connector
import datetime

def check_team_schedules():
    """
    Check if team objects have schedule information for H2H matchups
    """
    league = espn_connector.get_league_connection()
    if not league:
        return
    
    # Pick first team to inspect
    team = league.teams[0]
    print(f"Team: {team.team_name}")
    print(f"Schedule type: {type(team.schedule)}")
    
    if isinstance(team.schedule, list):
        print(f"Schedule length: {len(team.schedule)}")
        print("\nFirst few schedule items:")
        for item in team.schedule[:5]:
            print(f"  {item}")
    
    # Check if league has matchup schedule method
    print(f"\n--- League Methods ---")
    methods = [m for m in dir(league) if 'schedule' in m.lower() or 'matchup' in m.lower()]
    for method in methods:
        print(f"  {method}")

if __name__ == "__main__":
    check_team_schedules()
