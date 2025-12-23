# NBA Fantasy H2H Category Analysis Tool

A professional-grade analysis suite designed for ESPN Fantasy Basketball. This tool moves beyond basic point totals, utilizing Z-Scores, Variance, and Predictive Modeling to help managers dominate 9-Category Head-to-Head (H2H) leagues.

---

## 🚀 Product Vision
To transform raw NBA box score data into actionable intelligence. The tool aims to reduce "Manager Fatigue" by automating data collection and providing a "Virtual GM" experience that predicts matchup outcomes and identifies high-value trade opportunities through statistical normalization.

---

## 🗺️ Product Roadmap

### Phase 1: Data Ingestion & Live Feeds [✅ COMPLETE]
**Vision:** *The Real-Time NBA Pulse*
* **[x] ESPN API Sync:** Secure connection to pull private league settings and live rosters.
* **[x] NBA News Aggregator:** Real-time integration of NBC Sports/Rotoworld feeds.
* **[x] Schedule Tracker:** 3-column analysis tracker for Current and Upcoming matchups with advantage indicators.
* **[x] League Standings:** Dynamic ranking table with Win % and Ties.

### Phase 2: Statistical Engine & Normalization [🚧 IN PROGRESS]
**Vision:** *The Context Layer*
* **[ ] Z-Score Calibration:** Normalizing player value across all 9 categories (PTS, REB, AST, STL, BLK, 3PM, FG%, FT%, TO).
* **[ ] League Power Matrix:** 12-team category heatmap.
* **[ ] Punt-Mode Toggle:** Dynamic re-ranking based on ignored categories.
* **[ ] Volatility Analysis:** Identifying "High-Variance" players for DFS and H2H.

### Phase 3: Infrastructure & Scalability [✅ COMPLETE]
**Vision:** *The Scalable Foundation*
* **[x] Next.js 15 Migration:** Replaced Streamlit with a modern, high-performance React frontend.
* **[x] FastAPI Backend:** User-aware API with dynamic token handling.
* **[x] Mobile-Responsive UI:** Premium dark-mode dashboard with orange-centric branding.
* **[x] Supabase Authentication:** Fully integrated login, signup, and settings management.
* **[x] Dynamic Multi-User Support:** Backend now fetches private league credentials per-user from Supabase.

### Phase 4: Intelligence & Deployment
**Vision:** *Decision Support at the Speed of News*
* **[ ] Deployment:** Hosting on Vercel/Railway for 24/7 access.
* **[ ] Injury Impact Alerts:** Automated logic that surfaces "Next Man Up" opportunities.
* **[ ] Optimization Dashboard:** Prioritizing "Today's Must-Do Moves."

---

## 🛠️ Technical Stack
* **Frontend:** Next.js 15 (App Router), Tailwind CSS 4, Framer Motion
* **Backend:** FastAPI (Python 3.10+), Supabase Auth/DB
* **Database:** Supabase (PostgreSQL)
* **Auth:** Supabase GoTrue
* **API Wrapper:** `espn-api` (Python)

---

## 🛠️ Installation & Setup
1. **Backend**: `cd backend && pip install -r requirements.txt && python -m uvicorn app.main:app --reload`
2. **Frontend**: `cd frontend && npm install && npm run dev`
3. **Env**: Setup `.env` with Supabase credentials. 