from src.data import espn_connector
import json

def deep_inspect_settings():
    league = espn_connector.get_league_connection()
    if not league:
        return

    print(f"Current Matchup Period: {league.currentMatchupPeriod}")
    
    # 1. Dump raw matchup_periods
    mps = getattr(league.settings, 'matchup_periods', {})
    print(f"\nMatchup Periods Keys: {list(mps.keys())[:5]}")
    print(f"Sample Value (Key='{league.currentMatchupPeriod}'): {mps.get(str(league.currentMatchupPeriod))}")

    # 2. Inspect a player's schedule to see current scoring period IDs
    # We need a player with a game today/soon
    # Let's use Free Agents to be safe/neutral, or just the first team
    team = league.teams[0]
    player = team.roster[0]
    
    print(f"\nPlayer: {player.name}")
    print("Sample Schedule Entries (ScoringPeriod -> Date):")
    count = 0
    
    # Just print 5 entries around "now"
    sorted_sched = sorted(player.schedule.items(), key=lambda x: x[1]['date'])
    import datetime
    today = datetime.datetime.now()
    
    for sp_id, info in sorted_sched:
        date = info['date']
        # Print if within 30 days of now
        if abs((date - today).days) < 10:
            print(f"  SP: {sp_id} -> {date}")
            
    print("\n------------------------------")
    print("Does Matchup Period map directly to Scoring Period?")
    # If the MP value is [9], and we see SPs like 60, 61... then no.
    # If we see SP 9 in the past, then MP 9 = SP 9 is weird.

if __name__ == "__main__":
    deep_inspect_settings()
