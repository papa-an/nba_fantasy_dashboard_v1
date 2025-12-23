from fastapi import APIRouter, HTTPException
from nba_api.stats.endpoints import leaguedashplayerstats, playergamelog
from nba_api.stats.static import players
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

router = APIRouter()

# --- Helper Functions ---

def get_advanced_player_stats():
    """
    Fetches league-wide player stats and calculates Z-scores (Standard Deviations) 
    for the 9-cat fantasy categories to determine value.
    """
    try:
        # Fetch stats for the current season
        # measure_type='Base' gives us the raw counting stats
        stats = leaguedashplayerstats.LeagueDashPlayerStats(per_mode_detailed='PerGame', season='2024-25').get_data_frames()[0]
        
        # Keep only relevant fantasy columns
        cols = ['PLAYER_ID', 'PLAYER_NAME', 'TEAM_ABBREVIATION', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FTM', 'FTA', 'FT_PCT', 'FG3M', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV']
        df = stats[cols].copy()

        # Filter: Remove players with very few games or minutes to reduce noise
        # (Optional: can make this dynamic later)
        # df = df[df['MIN'] > 15] 

        # --- 9-Cat Z-Score Calculation ---
        # We calculate how many standard deviations a player is from the average.
        # This standardizes value across different categories (e.g., 2 blocks is worth more than 2 points).
        
        categories = {
            'PTS': 'PTS',
            'REB': 'REB',
            'AST': 'AST',
            'STL': 'STL',
            'BLK': 'BLK',
            'FG3M': 'FG3M',
            'TOV': 'TOV', # Negative value
            'FG_PCT': 'FG_PCT',
            'FT_PCT': 'FT_PCT'
        }

        z_score_cols = []
        
        for cat_name, col_name in categories.items():
            mean = df[col_name].mean()
            std = df[col_name].std()
            
            z_col = f'{cat_name}_Z'
            
            if cat_name == 'TOV':
                # For turnovers, fewer is better, so we invert the Z-score
                df[z_col] = (mean - df[col_name]) / std
            else:
                df[z_col] = (df[col_name] - mean) / std
                
            z_score_cols.append(z_col)

        # Total Value (Sum of Z-scores)
        df['TOTAL_Z'] = df[z_score_cols].sum(axis=1)
        
        # Rank by Total Z-Score
        df = df.sort_values(by='TOTAL_Z', ascending=False).reset_index(drop=True)
        df['RANK'] = df.index + 1

        return df.to_dict(orient='records')

    except Exception as e:
        print(f"Error fetching NBA stats: {e}")
        return []

def get_player_consistency(player_id, last_n_games=10):
    """
    Analyzes a specific player's variance over the last N games.
    """
    try:
        gamelog = playergamelog.PlayerGameLog(player_id=player_id, season='2024-25').get_data_frames()[0]
        recent_games = gamelog.head(last_n_games)
        
        # Calculate consistency (Standard Deviation of their fantasy points or key stats)
        # Lower std dev = more consistent
        
        stats_variance = {
            'PTS_VAR': recent_games['PTS'].var(),
            'PTS_STD': recent_games['PTS'].std(),
            'MIN_AVG': recent_games['MIN'].mean()
        }
        
        return stats_variance
    except Exception as e:
        return {}

# --- Endpoints ---

@router.get("/rankings")
async def get_player_rankings():
    """Returns all players ranked by 9-cat Z-score value."""
    stats = get_advanced_player_stats()
    if not stats:
        raise HTTPException(status_code=500, detail="Failed to fetch NBA stats")
    return stats[:200] # Return top 200 for now to keep payload light

@router.get("/player/{player_id}/consistency")
async def get_player_consistency_stats(player_id: int):
    """
    Returns consistency metrics (Standard Deviation) for a player's last 20 games.
    """
    try:
        # Fetch game logs
        gamelog = playergamelog.PlayerGameLog(player_id=player_id, season='2024-25').get_data_frames()[0]
        
        if gamelog.empty:
             return {"message": "No games played"}
             
        recent = gamelog.head(20) # Analyze last 20 games for relevant trend
        
        # Calculate Standard Deviation (Volatility) for 9-cat
        # Lower Clean_STD = Better Consistency
        stats_std = {
            'PTS_STD': round(recent['PTS'].std(), 2),
            'REB_STD': round(recent['REB'].std(), 2),
            'AST_STD': round(recent['AST'].std(), 2),
            'STL_STD': round(recent['STL'].std(), 2),
            'BLK_STD': round(recent['BLK'].std(), 2),
            'FG3M_STD': round(recent['FG3M'].std(), 2),
            'FG_PCT_STD': round(recent['FG_PCT'].std(), 3),
            'FT_PCT_STD': round(recent['FT_PCT'].std(), 3),
            'TOV_STD': round(recent['TOV'].std(), 2),
        }
        
        # Calculate a "Consistency Grade" (A-F) based on PTS volatility relative to average
        avg_pts = recent['PTS'].mean()
        cv_pts = stats_std['PTS_STD'] / avg_pts if avg_pts > 0 else 0
        
        grade = "B"
        if cv_pts < 0.2: grade = "A+" # Very consistent
        elif cv_pts < 0.3: grade = "A"
        elif cv_pts < 0.4: grade = "B"
        elif cv_pts < 0.5: grade = "C"
        else: grade = "D" # High volatility (Boom/Bust)

        return {
            "player_id": player_id,
            "games_analyzed": len(recent),
            "consistency_grade": grade,
            "volatility_stats": stats_std,
            "recent_averages": {
                "PTS": round(avg_pts, 1),
                "MIN": round(recent['MIN'].mean(), 1)
            }
        }
            
    except Exception as e:
        print(f"Error fetching consistency: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze consistency")

@router.get("/trending")
async def get_trending_players():
    """
    Identifies players with significant changes in minutes or usage 
    over the last 7 days compared to season average.
    """
    # Placeholder logic for now - implementation requires fetching gamelogs for all active players
    # which is heavy. We will optimize this in step 2.
    return {"message": "Trending player analysis coming soon"}
