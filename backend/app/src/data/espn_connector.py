from espn_api.basketball import League
from app.src.utils import config

def get_league_connection():
    """
    Establishes a connection to the ESPN Fantasy Basketball League.
    Returns a League object or raises an error if connection fails.
    """
    try:
        if not config.LEAGUE_ID:
            raise ValueError("LEAGUE_ID not found in environment variables.")
        
        # Initialize League
        league = League(
            league_id=int(config.LEAGUE_ID),
            year=config.SEASON,
            espn_s2=config.ESPN_S2,
            swid=config.SWID
        )
        return league
    except Exception as e:
        print(f"Failed to connect to ESPN League: {e}")
        return None

def fetch_teams(league):
    """
    Returns a list of teams from the league object.
    """
    if league:
        return league.teams
    return []
