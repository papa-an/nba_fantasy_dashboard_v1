# NBA Fantasy Scouting Suite (Pivot 2.0)

A professional-grade NBA scouting and analysis tool powered by public data. This tool replaces the "League Manager" concept with a "Pro Scout" experience, focusing on player value, consistency, and injury impact analysis using advanced statistical modeling.

---

## 🚀 Product Vision
To build the ultimate "Fantasy War Room" that doesn't rely on private league APIs. By using public NBA data, we provide deeper, faster, and more reliable insights: Z-Score rankings, consistency ratings, and injury impact reports that tell you who to pickup *before* your opponents do.

---

## 🗺️ Product Roadmap

### Phase 1: The Foundation (Data & Infra) [✅ COMPLETE]
**Vision:** *Robust, Public Data Pipeline*
* **[x] Next.js 15 & FastAPI Stack:** Modern, high-performance web architecture.
* **[x] Supabase Auth:** Secure user management.
* **[x] News Aggregator:** Real-time NBA news feed.
* **[x] Mobile-Responsive UI:** Premium dark-mode dashboard.
* **[x] Vercel & Render Deployment:** Production-ready hosting.

### Phase 2: Statistical Intelligence [🚧 IN PROGRESS]
**Vision:** *Moneyball for Fantasy*
* **[ ] NBA API Integration:** Replaced ESPN dependency with `nba_api`.
* **[ ] Z-Score Engine:** 9-Category value normalization (Standard Deviation analysis).
* **[ ] Consistency Ratings:** "Variance Cards" showing player reliability (High/Low variation).
* **[ ] Player Rankings:** Dynamic sorting by specific stat categories or total value.

### Phase 3: The "War Room" Experience [📅 UPCOMING]
**Vision:** *Actionable Insights*
* **[ ] Injury Impact Analysis:** "Next Man Up" logic identifying bench players who gain value when starters sit.
* **[ ] Trend Tracker:** Identifying players with spiked usage/minutes in the last 7 days.
* **[ ] Trade Rumor Mill:** Aggregating social media and trade report buzz.
* **[ ] Team Depth Charts:** Visualizing rotations and opportunity voids.

### Phase 4: AI & Personalization
**Vision:** *Your Virtual Assistant GM*
* **[ ] AI Scouting Reports:** Generated narratives on player performance.
* **[ ] Watchlist Alerts:** Custom notifications for tracked players.
* **[ ] Comparison Tool:** Side-by-side player metric showdowns.

---

## 🛠️ Technical Stack
* **Frontend:** Next.js 15 (App Router), Tailwind CSS 4, Framer Motion
* **Backend:** FastAPI (Python 3.10+), `nba_api`, `pandas`, `numpy`
* **Database:** Supabase (PostgreSQL)
* **Auth:** Supabase GoTrue

---

## 🛠️ Installation & Setup
1. **Backend**: `cd backend && pip install -r requirements.txt && python -m uvicorn app.main:app --reload`
2. **Frontend**: `cd frontend && npm install && npm run dev`
 