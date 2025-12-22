from espn_api.basketball import League
from src.utils import config
import streamlit as st

def get_league_connection():
    """
    Establishes a connection to the ESPN Fantasy Basketball League.
    Returns a League object or raises an error if connection fails.
    """
    try:
        if not config.LEAGUE_ID:
            raise ValueError("LEAGUE_ID not found in environment variables.")
        
        # Initialize League
        # If public league, swid and espn_s2 are not strictly required, but usually needed for specialized data
        # If private, they are mandatory.
        league = League(
            league_id=int(config.LEAGUE_ID),
            year=config.SEASON,
            espn_s2=config.ESPN_S2,
            swid=config.SWID
        )
        return league
    except Exception as e:
        st.error(f"Failed to connect to ESPN League: {e}")
        return None

def fetch_teams(league):
    """
    Returns a list of teams from the league object.
    """
    if league:
        return league.teams
    return []
