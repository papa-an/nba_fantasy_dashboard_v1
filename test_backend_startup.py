import sys
import os

try:
    print("Testing imports...")
    from fastapi import FastAPI
    from nba_api.stats.endpoints import leaguedashplayerstats
    import pandas as pd
    import numpy as np
    from app.main import app
    print("Imports success!")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
