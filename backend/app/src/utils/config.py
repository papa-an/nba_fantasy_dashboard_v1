import os
from dotenv import load_dotenv

# Try to find .env in current, parent, or parent's parent directory
def load_env_robust():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Walk up to 6 levels to find .env
    for _ in range(6):
        dotenv_path = os.path.join(current_dir, '.env')
        if os.path.exists(dotenv_path):
            print(f"DEBUG: Found .env at {dotenv_path}")
            load_dotenv(dotenv_path)
            return True
        current_dir = os.path.dirname(current_dir)
    return False

load_env_robust()

def get_config(key, default=None):
    return os.getenv(key, default)

LEAGUE_ID = get_config("LEAGUE_ID")
SEASON = int(get_config("Season", 2025)) # Fallback to 2025
ESPN_S2 = get_config("ESPN_S2")
SWID = get_config("SWID")

print(f"DEBUG: Config Loaded - League: {LEAGUE_ID}, Season: {SEASON}")
