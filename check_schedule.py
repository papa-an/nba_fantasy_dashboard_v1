from src.data import espn_connector

league = espn_connector.get_league_connection()
team = league.teams[3]  # North Bay Mamba

print(f"Team: {team.team_name}")
print(f"\nSchedule for periods 10-12 (indices 9-11):\n")

for idx in [9, 10, 11]:
    m = team.schedule[idx]
    period = idx + 1
    home = m.home_team.team_name if m.home_team else "BYE"
    away = m.away_team.team_name if m.away_team else "BYE"
    
    # Determine opponent
    if home == team.team_name:
        opponent = away
    else:
        opponent = home
    
    print(f"Period {period}: vs {opponent}")
