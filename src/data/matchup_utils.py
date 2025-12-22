def get_matchups_from_team_schedules(league, matchup_period):
    """
    Build matchup pairs from team schedules instead of relying on league.box_scores().
    Returns a list of tuples: [(home_team, away_team), ...]
    """
    matchups = {}
    
    # The matchup_period corresponds to schedule index (period - 1)
    schedule_idx = matchup_period - 1
    
    for team in league.teams:
        if schedule_idx >= len(team.schedule):
            continue
            
        matchup = team.schedule[schedule_idx]
        
        # Get home and away teams
        home_team = matchup.home_team
        away_team = matchup.away_team
        
        if not home_team or not away_team:
            continue  # BYE week
        
        # Create a unique key for this matchup (sorted team IDs)
        key = tuple(sorted([home_team.team_id, away_team.team_id]))
        
        # Store matchup (avoid duplicates)
        if key not in matchups:
            matchups[key] = (home_team, away_team)
    
    return list(matchups.values())
