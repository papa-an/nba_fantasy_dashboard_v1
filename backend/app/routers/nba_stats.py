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
        
        # Calculate Standard Deviation (Volatility) for 9-cat and normalize it
        # using Coefficient of Variation (CV = std / mean) to give a rating.
        stats_data = {}
        
        categories = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG3M', 'FG_PCT', 'FT_PCT', 'TOV']
        
        for cat in categories:
            val_mean = recent[cat].mean()
            val_std = recent[cat].std()
            
            # Avoid division by zero
            cv = (val_std / val_mean) if val_mean > 0.1 else 0.0
            
            # Rating Logic (CV thresholds)
            # These thresholds might need tuning
            rating = "Stable"
            color = "blue"
            
            if cv < 0.15:
                rating = "Elite"
                color = "green"
            elif cv < 0.30:
                rating = "Stable"
                color = "blue"
            elif cv < 0.50:
                rating = "Volatile"
                color = "yellow"
            else:
                rating = "Wild"
                color = "red"
                
            # Special case for percentages with low volume
            if cat in ['FG_PCT', 'FT_PCT'] and val_mean < 0.1:
                rating = "Low Vol"
                color = "gray"

            stats_data[cat] = {
                "std": round(val_std, 2),
                "mean": round(val_mean, 1),
                "cv": round(cv, 2),
                "rating": rating,
                "color": color
            }

        # Calculate a "Consistency Grade" (A-F) based on PTS volatility mainly,
        # but could ideally be an average of all CVs.
        avg_pts = recent['PTS'].mean()
        cv_pts = stats_data['PTS']['cv']
        
        grade = "B"
        if cv_pts < 0.15: grade = "A+" 
        elif cv_pts < 0.25: grade = "A"
        elif cv_pts < 0.35: grade = "B"
        elif cv_pts < 0.50: grade = "C"
        else: grade = "F"

        return {
            "player_id": player_id,
            "games_analyzed": len(recent),
            "consistency_grade": grade,
            "volatility_stats": stats_data, # New detailed structure
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
