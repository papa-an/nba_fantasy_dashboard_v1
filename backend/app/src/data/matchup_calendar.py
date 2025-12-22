import datetime

def get_season_start_date(season_year):
    """
    Returns the start date of the NBA season for the given 'ending' year.
    E.g. Season 2026 ends in 2026, starts in Oct 2025.
    """
    if season_year == 2026:
        return datetime.date(2025, 10, 21) # Based on user screenshot
    # Fallback to standard late Oct
    return datetime.date(season_year - 1, 10, 22)

def get_matchup_schedule(season_year=2026):
    """
    Returns a dictionary mapping MatchupID (int) -> (start_date, end_date).
    Handles the 2025-26 season specifically based on user schedule.
    """
    # Start Date
    start_date = get_season_start_date(season_year)
    
    schedule = {}
    current_start = start_date
    
    # Matchup 1 is usually partial week (Tue-Sun) or user's specific Mon-Sun
    # Screenshot says Oct 21 (Tue) - Oct 26 (Sun)
    # But usually fantasy weeks run Mon-Sun.
    # Let's assume M1 ends on the first Sunday.
    
    # Iterate for 25 weeks roughly
    for matchup_id in range(1, 25):
        # Determine duration
        duration = 7 # Default 7 days
        
        # Exceptions (All Star Break)
        # In 2026, ASB is likely around Feb 15.
        # Screenshot says Matchup 17 (Feb 9 - 22). That's 14 days.
        if matchup_id == 17:
             duration = 14
        
        # M1 Duration: Oct 21 to Oct 26 is 6 days.
        if matchup_id == 1:
            # We can calculate end date as next Sunday
            # Oct 21 2025 is Tuesday.
            # Sunday is Oct 26.
            # Duration = 6 days (inclusive).
            duration = 6
        
        # Calculate End Date
        # Start + Duration - 1 (since inclusive)
        # ex: Start Mon, Dur 7 -> End Sun. 
        # But if Start is Tue (M1) and end Sun?
        
        # Let's do: End is always Sunday?
        # M1: Oct 21 -> Oct 26 (Sun).
        # M2: Oct 27 (Mon) -> ...
        
        if matchup_id == 1:
            # Hardcode M1 end
            current_end = datetime.date(2025, 10, 26)
        elif matchup_id == 17:
             # Feb 9 + 13 days = Feb 22 (Sunday)
             current_end = current_start + datetime.timedelta(days=13)
        else:
             # Standard week: Mon -> Sun (6 days delta)
             current_end = current_start + datetime.timedelta(days=6)
             
        schedule[matchup_id] = (current_start, current_end)
        
        # Prepare next start
        current_start = current_end + datetime.timedelta(days=1)
        
    return schedule

def get_current_matchup_period_id(schedule, target_date=None):
    if target_date is None:
        target_date = datetime.date.today()
        
    for mid, (start, end) in schedule.items():
        if start <= target_date <= end:
            return mid
            
    return 1 # Fallback
