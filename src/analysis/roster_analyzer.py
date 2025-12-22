def generate_roster_insight(roster):
    """
    Analyzes a roster to generate basic strategic insights based on position counts.
    Returns a dictionary with a concise summary string.
    """
    
    # Basic Count
    guards = 0
    forwards = 0
    centers = 0
    total_players = len(roster)
    
    # Positional Mapping (Simple heuristic)
    # ESPN positions can be complicated (e.g., 'PG, SG'), so we count occurrences
    for player in roster:
        pos = player.position
        if 'PG' in pos or 'SG' in pos:
            guards += 1
        if 'SF' in pos or 'PF' in pos:
            forwards += 1
        if 'C' in pos:
            centers += 1
            
    # Determine Composition
    # Note: A player like 'pg, sg' counts as 1 guard in logic above if we used elif, 
    # but here we just check mapped slots. Let's keep it simple.
    
    insight_text = ""
    
    insight_text = ""
    win_strategy = ""
    improvement_plan = ""
    
    # Composition Logic
    if guards > forwards and guards > centers:
        composition = "Guard-Heavy Small Ball"
        likely_punt = "Block/Rebound"
        strength = "FT%, 3PM, AST, STL"
        
        # HTML Bold tags used for guaranteed rendering in Streamlit HTML container
        report_text = (
            f"This team runs a <b>{composition}</b> strategy. With {guards} guards and only {centers} centers, "
            f"they excel in <b>{strength}</b> while likely punting <b>{likely_punt}</b>."
        )
        
        win_strategy = (
            "<b>Running small?</b> Lean into it. Stream high-efficiency guards to lock down FT% and steals. "
            "Don't chase rebounds against big teams; focus on winning 5-4 with efficiency and assists."
        )
        
        improvement_plan = (
            "<b>Need balance?</b> Trade a high-assist guard for a block-specialist forward to shore up FG% and BLK "
            "without sacrificing your FT% advantage."
        )
        
    elif centers >= 3 and centers > guards:
        composition = "Big Man Dominant"
        likely_punt = "FT%, 3PM"
        strength = "FG%, REB, BLK"
        
        report_text = (
            f"This team is <b>{composition}</b>. With {centers} centers, the foundation is built on "
            f"<b>{strength}</b>, likely accepting a punt on <b>{likely_punt}</b>."
        )
        
        win_strategy = (
            "<b>Bully Ball.</b> Secure FG% and Rebounds early in the week. Stream blocks specialists on off-days "
            "to ensure you dominate the paint categories."
        )
        
        improvement_plan = (
            "<b>Too one-dimensional?</b> Look for 'out-of-position' stats. A center who hits 3s (e.g., Myles Turner) "
            "or gets assists (e.g., Sabonis) adds massive value to this build."
        )
        
    else:
        composition = "Balanced Build"
        likely_punt = "None (Balanced)"
        strength = "Balanced across categories"
        
        report_text = (
            f"This is a <b>{composition}</b>. The roster is well-distributed ({guards}G / {forwards}F / {centers}C), "
            f"aiming to compete in all 9 categories without a hard punt."
        )
        
        win_strategy = (
            "<b>Flexibility is key.</b> Your balanced roster allows you to pivot mid-week. "
            "Identify your opponent's weakest category on Wednesday and stream specifically to steal it."
        )
        
        improvement_plan = (
            "<b>Jack of all trades, master of none?</b> Consider consolidating 2 good players into 1 elite star "
            "to open a streaming spot and define a stronger team identity."
        )
    
    return {
        "composition_report": report_text,
        "win_strategy": win_strategy,
        "improvement_plan": improvement_plan,
        "composition_title": composition
    }
