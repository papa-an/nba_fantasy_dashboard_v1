from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from app.routers import news, nba_stats

try:
    from supabase import create_client, Client
    supabase_installed = True
except ImportError:
    supabase_installed = False
    Client = object # Dummy class for type hinting


# Load environment variables from .env file FIRST
load_dotenv()

app = FastAPI(title="NBA Fantasy Intelligence API")

# Include Routers
app.include_router(news.router, prefix="/news", tags=["News"])
app.include_router(nba_stats.router, prefix="/nba", tags=["NBA Stats"])

# Supabase Client (Optional for now, but kept for future user features like watchlists)
supabase_url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

supabase: Client = None
if supabase_installed and supabase_url and supabase_key:
    supabase = create_client(supabase_url, supabase_key)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "NBA Fantasy Intelligence",
        "supabase": bool(supabase)
    }

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://nba-fantasy-dashboard-v1.vercel.app",
]

# Allow all Vercel preview deployments
allow_origin_regex = r"https://nba-fantasy-dashboard-v1-.*\.vercel\.app"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=allow_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
