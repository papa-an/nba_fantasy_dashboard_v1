import datetime
from collections import defaultdict

def get_week_dates(offset_days=0):
    """
    Returns a list of datetime.date objects for a week (Monday - Sunday).
    offset_days: 0 for current week, 7 for next week, etc.
    """
    today = datetime.date.today() + datetime.timedelta(days=offset_days)
    start_of_week = today - datetime.timedelta(days=today.weekday())
    week_dates = [start_of_week + datetime.timedelta(days=i) for i in range(7)]
    return week_dates

def count_games_in_range(roster, start_date, end_date):
    """
    Counts games for a roster within a date range.
    Returns:
    - total_games (int)
    - daily_counts (dict): {date_obj: count}
    """
    total_games = 0
    daily_counts = defaultdict(int)
    
    # Ensure range covers full days
    # Convert dates to check easily
    target_dates = set()
    curr = start_date
    while curr <= end_date:
        target_dates.add(curr)
        curr += datetime.timedelta(days=1)
        
    for player in roster:
        # Check player.schedule
        # Structure: {'scoringPeriodId': {'team': 'OPP', 'date': datetime_obj}}
        if not hasattr(player, 'schedule') or not player.schedule:
            continue
            
        for _, game_info in player.schedule.items():
            game_date = game_info.get('date')
            # Handle if date is datetime
            if isinstance(game_date, datetime.datetime):
                game_date = game_date.date()
                
            if game_date in target_dates:
                total_games += 1
                daily_counts[game_date] += 1
                
    return total_games, daily_counts
