import os
from dotenv import load_dotenv

# Load environment variables from .env file
# Root is 4 levels up: src/utils/config.py -> utils -> src -> app -> backend -> root
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), '.env')
load_dotenv(dotenv_path)

def get_config(key, default=None):
    return os.getenv(key, default)

LEAGUE_ID = get_config("LEAGUE_ID")
# Default to current year if not specified. Note: ESPN API uses the year the season *ends*.
# So for 2024-2025 season, use 2025.
SEASON = int(get_config("Season", 2026))
ESPN_S2 = get_config("ESPN_S2")
SWID = get_config("SWID")
