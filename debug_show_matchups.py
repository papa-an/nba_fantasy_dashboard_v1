from src.data import espn_connector, matchup_calendar
from src.utils import config
import datetime

def show_all_upcoming_matchups():
    league = espn_connector.get_league_connection()
    if not league:
        return

    # Calculate current matchup based on date
    schedule_map = matchup_calendar.get_matchup_schedule(season_year=config.SEASON)
    today = datetime.date.today()
    current_matchup_id = matchup_calendar.get_current_matchup_period_id(schedule_map, today)
    
    print(f"Today: {today}")
    print(f"Current Matchup: {current_matchup_id} ({schedule_map[current_matchup_id][0]} to {schedule_map[current_matchup_id][1]})")
    
    # Show matchups for periods 10, 11, 12
    for period in [10, 11, 12]:
        if period in schedule_map:
            start, end = schedule_map[period]
            print(f"\n--- Matchup {period} ({start} to {end}) ---")
            try:
                box_scores = league.box_scores(matchup_period=period)
                for box in box_scores:
                    print(f"  {box.home_team.team_name} vs {box.away_team.team_name}")
            except Exception as e:
                print(f"  Error: {e}")

if __name__ == "__main__":
    show_all_upcoming_matchups()
