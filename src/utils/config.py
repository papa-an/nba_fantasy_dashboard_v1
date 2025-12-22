import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_config(key, default=None):
    return os.getenv(key, default)

LEAGUE_ID = get_config("LEAGUE_ID")
# Default to current year if not specified. Note: ESPN API uses the year the season *ends*.
# So for 2024-2025 season, use 2025.
SEASON = int(get_config("Season", 2025))
ESPN_S2 = get_config("ESPN_S2")
SWID = get_config("SWID")
