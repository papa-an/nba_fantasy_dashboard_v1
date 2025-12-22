from src.data import espn_connector, matchup_utils

league = espn_connector.get_league_connection()

print("Testing matchup_utils for periods 10-12:\n")

for period in [10, 11, 12]:
    print(f"--- Period {period} ---")
    matchups = matchup_utils.get_matchups_from_team_schedules(league, period)
    for home, away in matchups:
        print(f"  {home.team_name} vs {away.team_name}")
    print()
