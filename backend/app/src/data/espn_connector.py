from espn_api.basketball import League
from app.src.utils import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_league_connection(league_id=None, season=None, espn_s2=None, swid=None):
    """
    Connects to the ESPN Fantasy League.
    Uses provided credentials or falls back to environment variables from config.
    """
    l_id = league_id or config.LEAGUE_ID
    s_yr = season or config.SEASON
    s2 = espn_s2 or config.ESPN_S2
    sw = swid or config.SWID
    
    # Validation
    if not l_id:
        logger.error("LEAGUE_ID is missing")
        return None

    logger.info(f"Attempting connection to League {l_id} for Season {s_yr}")
    
    try:
        if s2 and sw:
            # Clean up potential whitespace or quotes from cookies
            s2 = s2.strip('"').strip("'")
            sw = sw.strip('"').strip("'")
            league = League(league_id=int(l_id), year=int(s_yr), espn_s2=s2, swid=sw)
        else:
            league = League(league_id=int(l_id), year=int(s_yr))
        
        # Test connection by accessing a simple property
        _ = league.settings.name
        return league
    except Exception as e:
        logger.error(f"ESPN Connection Error: {str(e)}")
        # If it fails with 2026, try 2025 as a secondary fallback
        if str(s_yr) == "2026":
            try:
                logger.info("Retrying with Season 2025...")
                league = League(league_id=int(l_id), year=2025, espn_s2=s2, swid=sw)
                _ = league.settings.name
                return league
            except Exception as retry_e:
                logger.error(f"Retry with 2025 failed: {str(retry_e)}")
        return None
