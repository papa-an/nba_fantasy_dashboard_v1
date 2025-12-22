import pandas as pd
import datetime
from app.src.data import schedule_engine, matchup_utils

def get_matchup_analysis(league, matchup_period, start_date, end_date, my_team_id=None):
    """
    Computes schedule analysis for a specific matchup period.
    Ported from schedule_view.py logic to be API-ready.
    """
    days_in_range = []
    curr = start_date
    while curr <= end_date:
        days_in_range.append(curr)
        curr += datetime.timedelta(days=1)
        
    day_headers = [d.strftime('%a') for d in days_in_range]
    day_dates = [d.isoformat() for d in days_in_range]
    
    matchup_pairs = matchup_utils.get_matchups_from_team_schedules(league, matchup_period)
    
    if not matchup_pairs:
        return None

    # Sort: My matchup first if team selected
    if my_team_id:
        matchup_pairs.sort(key=lambda pair: (pair[0].team_id == my_team_id or pair[1].team_id == my_team_id), reverse=True)

    results = []
    
    for home_team, away_team in matchup_pairs:
        home_total, home_daily = schedule_engine.count_games_in_range(home_team.roster, start_date, end_date)
        away_total, away_daily = schedule_engine.count_games_in_range(away_team.roster, start_date, end_date)
        
        diff = home_total - away_total
        
        # Advantage calculation
        advantage_message = "Even"
        if diff > 0:
            advantage_message = f"{home_team.team_name} +{diff}"
        elif diff < 0:
            advantage_message = f"{away_team.team_name} +{abs(diff)}"
            
        is_my_matchup = False
        if my_team_id:
            is_my_matchup = (home_team.team_id == my_team_id or away_team.team_id == my_team_id)

        results.append({
            "home_team": {
                "id": home_team.team_id,
                "name": home_team.team_name,
                "total_games": home_total,
                "daily_counts": [home_daily.get(d, 0) for d in days_in_range]
            },
            "away_team": {
                "id": away_team.team_id,
                "name": away_team.team_name,
                "total_games": away_total,
                "daily_counts": [away_daily.get(d, 0) for d in days_in_range]
            },
            "diff": diff,
            "advantage_message": advantage_message,
            "is_my_matchup": is_my_matchup
        })
        
    return {
        "period": matchup_period,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "days": day_headers,
        "day_dates": day_dates,
        "matchups": results
    }
