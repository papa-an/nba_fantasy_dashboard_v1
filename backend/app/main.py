from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import pandas as pd
import datetime

# Import legacy logic (will need refactoring internally to remove streamlit)
from app.src.data import espn_connector, news_aggregator, schedule_engine, matchup_calendar
from app.src.analysis import roster_analyzer
from app.src.utils import config

from app.services import matchup_service

app = FastAPI(title="NBA Fantasy API")

# Configure CORS for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "NBA Fantasy API is running"}

@app.get("/league/info")
async def get_league_info():
    league = espn_connector.get_league_connection()
    if not league:
        raise HTTPException(status_code=400, detail="Could not connect to ESPN League")
    
    return {
        "name": league.settings.name,
        "season": config.SEASON,
        "teams_count": len(league.teams)
    }

@app.get("/league/standings")
async def get_standings():
    league = espn_connector.get_league_connection()
    if not league:
        raise HTTPException(status_code=400, detail="Could not connect to ESPN League")
    
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
async def get_teams():
    league = espn_connector.get_league_connection()
    if not league:
        raise HTTPException(status_code=400, detail="Could not connect to ESPN League")
    
    return [{"id": t.team_id, "name": t.team_name} for t in league.teams]

@app.get("/team/{team_id}/roster")
async def get_roster(team_id: int):
    league = espn_connector.get_league_connection()
    if not league:
        raise HTTPException(status_code=400, detail="Could not connect to ESPN League")
    
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
    news_items = news_aggregator.fetch_player_news()
    return news_items

@app.get("/schedule/current")
async def get_current_schedule(my_team_id: Optional[int] = None):
    league = espn_connector.get_league_connection()
    if not league:
        raise HTTPException(status_code=400, detail="Could not connect to ESPN League")
    
    schedule_map = matchup_calendar.get_matchup_schedule(season_year=config.SEASON)
    today = datetime.date.today()
    matchup_id = matchup_calendar.get_current_matchup_period_id(schedule_map, today)
    
    start_date, end_date = schedule_map[matchup_id]
    
    analysis = matchup_service.get_matchup_analysis(
        league, matchup_id, start_date, end_date, my_team_id
    )
    
    return analysis

@app.get("/schedule/upcoming")
async def get_upcoming_schedule(my_team_id: Optional[int] = None):
    league = espn_connector.get_league_connection()
    if not league:
        raise HTTPException(status_code=400, detail="Could not connect to ESPN League")
    
    schedule_map = matchup_calendar.get_matchup_schedule(season_year=config.SEASON)
    today = datetime.date.today()
    current_matchup_id = matchup_calendar.get_current_matchup_period_id(schedule_map, today)
    next_matchup_id = current_matchup_id + 1
    
    if next_matchup_id not in schedule_map:
        raise HTTPException(status_code=404, detail="Upcoming matchup not found")
        
    start_date, end_date = schedule_map[next_matchup_id]
    
    analysis = matchup_service.get_matchup_analysis(
        league, next_matchup_id, start_date, end_date, my_team_id
    )
    
    return analysis
