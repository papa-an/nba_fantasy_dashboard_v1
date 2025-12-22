from src.data import espn_connector, matchup_calendar
from src.utils import config
import datetime

def debug_future_matchups():
    league = espn_connector.get_league_connection()
    if not league:
        return

    # Calculate current matchup based on date
    schedule_map = matchup_calendar.get_matchup_schedule(season_year=config.SEASON)
    today = datetime.date.today()
    current_matchup_id = matchup_calendar.get_current_matchup_period_id(schedule_map, today)
    
    print(f"Today: {today}")
    print(f"Calculated Current Matchup ID: {current_matchup_id}")
    print(f"ESPN API Current Matchup Period: {league.currentMatchupPeriod}")
    
    # Try to get box scores for next matchup
    next_matchup_id = current_matchup_id + 1
    print(f"\n--- Fetching Box Scores for Matchup {next_matchup_id} ---")
    
    try:
        box_scores_next = league.box_scores(matchup_period=next_matchup_id)
        print(f"Found {len(box_scores_next)} matchups for period {next_matchup_id}")
        
        # Print all matchups
        for box in box_scores_next:
            print(f"  {box.home_team.team_name} vs {box.away_team.team_name}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    # Also check the league schedule attribute if available
    print(f"\n--- Checking League Teams ---")
    for team in league.teams:
        print(f"{team.team_name} (Team ID: {team.team_id})")
        if hasattr(team, 'schedule'):
            print(f"  Has schedule attribute: {type(team.schedule)}")

if __name__ == "__main__":
    debug_future_matchups()
