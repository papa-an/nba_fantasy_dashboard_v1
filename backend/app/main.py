from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import pandas as pd
import datetime
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from app.routers import news, nba_stats

# Load environment variables from .env file FIRST
load_dotenv()

# Import legacy logic
from app.src.data import espn_connector, news_aggregator, schedule_engine, matchup_calendar
from app.src.analysis import roster_analyzer
from app.src.utils import config
from app.services import matchup_service

app = FastAPI(title="NBA Fantasy API")

# Include Routers
app.include_router(news.router, prefix="/news", tags=["News"])
app.include_router(nba_stats.router, prefix="/nba", tags=["NBA Stats"])

# Supabase Admin Client for fetching user settings
supabase_url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

print(f"DEBUG: Supabase URL: {supabase_url}")
print(f"DEBUG: Supabase Key Present: {bool(supabase_key)}")

if not supabase_url or not supabase_key:
    print("CRITICAL: Missing Supabase environment variables!")

supabase: Client = create_client(supabase_url, supabase_key) if supabase_url and supabase_key else None

# Backend Caching Logic
# Store objects: { user_id: { "league": LeagueObj, "expires": timestamp } }
_league_cache = {}
CACHE_EXPIRY_SECONDS = 600 # 10 Minutes

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "supabase": bool(supabase),
        "env": {
            "url": bool(os.getenv("NEXT_PUBLIC_SUPABASE_URL")),
            "key": bool(os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY"))
        }
    }

async def get_current_user_league(authorization: str = Header(None)):
    """
    Dependency to get the ESPN League connection for the authenticated user.
    """
    if not authorization or authorization == "Bearer undefined":
        # For local development without auth or when frontend hasn't loaded token
        print("DEBUG: No auth header or undefined. Falling back to .env credentials.")
        league = espn_connector.get_league_connection()
        if not league:
            raise HTTPException(status_code=401, detail="Authentication required or .env credentials missing")
        return league

    if not supabase:
        print("CRITICAL: Supabase client not initialized. Check your .env file.")
        raise HTTPException(status_code=500, detail="Backend configuration error (Supabase missing)")

    try:
        token = authorization.replace("Bearer ", "")
        
        # 1. Check Cache first
        now = datetime.datetime.now().timestamp()
        # Note: We use the token as part of the key if we want to be safe, but user_id is better
        # For now, let's just get the user first.
        
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
            raise HTTPException(status_code=401, detail="Invalid session")
        
        user_id = user_response.user.id

        if user_id in _league_cache:
            cache_entry = _league_cache[user_id]
            if now < cache_entry["expires"]:
                return cache_entry["league"]

        # 2. Fetch settings
        settings_response = supabase.table("league_settings").select("*").eq("id", user_id).execute()
        if not settings_response.data:
            raise HTTPException(status_code=400, detail="No ESPN credentials found. Please go to Settings.")
        
        s = settings_response.data[0]
        
        # Log what we're trying
        print(f"DEBUG: Connecting to ESPN - League: {s.get('league_id')}, Season: {s.get('season')}")
        
        try:
            league = espn_connector.get_league_connection(
                league_id=s.get('league_id'),
                season=s.get('season'),
                espn_s2=s.get('espn_s2'),
                swid=s.get('swid')
            )
        except Exception as espn_err:
            error_detail = f"ESPN Connection Failed: {str(espn_err)}"
            print(f"ERROR: {error_detail}")
            raise HTTPException(status_code=400, detail=error_detail)
        
        if not league:
            raise HTTPException(status_code=400, detail="Could not connect to ESPN. Check your credentials in Settings.")

        # Update Cache
        _league_cache[user_id] = {
            "league": league,
            "expires": now + CACHE_EXPIRY_SECONDS
        }
            
        return league
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_current_user_league: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")

# Configure CORS - Allow localhost and all Vercel deployments
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^https://.*\.vercel\.app$|^http://(localhost|127\.0\.0\.1):3000$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "NBA Fantasy API is running"}

@app.get("/league/info")
async def get_league_info(league=Depends(get_current_user_league)):
    return {
        "name": league.settings.name,
        "season": league.year,
        "teams_count": len(league.teams)
    }

@app.get("/league/standings")
async def get_standings(league=Depends(get_current_user_league)):
    standings = []
    for team in league.teams:
        total_games = team.wins + team.losses + team.ties
        win_pct = team.wins / total_games if total_games > 0 else 0.0
        standings.append({
            "id": team.team_id,
            "name": team.team_name,
            "owner": team.owners[0].get('firstName', 'Unknown') if team.owners else 'Unknown',
            "wins": team.wins,
            "losses": team.losses,
            "ties": team.ties,
            "win_pct": round(win_pct, 3),
            "rank": team.standing
        })
    return sorted(standings, key=lambda x: x['rank'])

@app.get("/league/teams")
async def get_teams(league=Depends(get_current_user_league)):
    return [{"id": t.team_id, "name": t.team_name} for t in league.teams]

@app.get("/team/{team_id}/roster")
async def get_roster(team_id: int, league=Depends(get_current_user_league)):
    team = next((t for t in league.teams if t.team_id == team_id), None)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    roster = []
    for player in team.roster:
        roster.append({
            "name": player.name,
            "position": player.position,
            "injury_status": player.injuryStatus,
            "acquisition_type": player.acquisitionType
        })
    
    insights = roster_analyzer.generate_roster_insight(team.roster)
    
    return {
        "team_name": team.team_name,
        "roster": roster,
        "insights": insights
    }

@app.get("/news")
async def get_news():
    # News is public/global
    news_items = news_aggregator.fetch_player_news()
    return news_items

@app.get("/schedule/current")
async def get_current_schedule(my_team_id: Optional[int] = None, league=Depends(get_current_user_league)):
    schedule_map = matchup_calendar.get_matchup_schedule(season_year=league.year)
    today = datetime.date.today()
    matchup_id = matchup_calendar.get_current_matchup_period_id(schedule_map, today)
    start_date, end_date = schedule_map[matchup_id]
    analysis = matchup_service.get_matchup_analysis(league, matchup_id, start_date, end_date, my_team_id)
    return analysis

@app.get("/schedule/upcoming")
async def get_upcoming_schedule(my_team_id: Optional[int] = None, league=Depends(get_current_user_league)):
    schedule_map = matchup_calendar.get_matchup_schedule(season_year=league.year)
    today = datetime.date.today()
    current_matchup_id = matchup_calendar.get_current_matchup_period_id(schedule_map, today)
    next_matchup_id = current_matchup_id + 1
    
    if next_matchup_id not in schedule_map:
        raise HTTPException(status_code=404, detail="Upcoming matchup not found")
        
    start_date, end_date = schedule_map[next_matchup_id]
    analysis = matchup_service.get_matchup_analysis(league, next_matchup_id, start_date, end_date, my_team_id)
    return analysis
