# NBA Fantasy H2H Category Analysis Tool

A professional-grade analysis suite designed for ESPN Fantasy Basketball. This tool moves beyond basic point totals, utilizing Z-Scores, Variance, and Predictive Modeling to help managers dominate 9-Category Head-to-Head (H2H) leagues.

---

## 🚀 Product Vision
To transform raw NBA box score data into actionable intelligence. The tool aims to reduce "Manager Fatigue" by automating data collection and providing a "Virtual GM" experience that predicts matchup outcomes and identifies high-value trade opportunities through statistical normalization.

---

## 🗺️ Product Roadmap

### Phase 1: Data Ingestion & Live Feeds
**Vision:** *The Real-Time NBA Pulse*
* **ESPN API Sync:** Secure connection via `swid` and `espn_s2` cookies to pull private league settings and live rosters.
* **NBA News Aggregator:** Real-time integration of Underdog NBA and Rotoworld feeds, filtered specifically for rostered players.
* **Schedule Tracker:** A "Games per Week" calculator to compare active roster volume against H2H opponents.

### Phase 2: Statistical Engine & Normalization
**Vision:** *The Context Layer*
* **Z-Score Calibration:** Normalizing player value across all 9 categories (PTS, REB, AST, STL, BLK, 3PM, FG%, FT%, TO).
    * *Formula:* $Z = \frac{x - \mu}{\sigma}$
* **Volatility & Variance Analysis:** Utilizing **Standard Deviation ($\sigma$)** to identify "High-Variance" (boom/bust) players vs. "Safe Floor" anchors.
* **Punt-Mode Toggle:** Dynamic re-ranking of players based on specific "Punt" strategies (e.g., Punting FT% or TO).

### Phase 3: Strategic Decision Engine
**Vision:** *The Virtual GM*
* **Trade Impact Simulator:** A "Before vs. After" visualization of how a trade shifts team Z-scores across all categories.
* **H2H Matchup Predictor:** Monte Carlo simulations of the upcoming week using Rest-of-Season (ROS) projections and strength of schedule.
* **Streaming Logic:** An automated waiver wire tool to find the best category-specific "streamers" based on daily game density.

### Phase 4: Proactive Intelligence (UI/UX)
**Vision:** *Decision Support at the Speed of News*
* **Interactive Heatmaps:** League-wide visual grids identifying which opponents are vulnerable in specific categories.
* **Injury Impact Alerts:** Automated logic that surfaces "Next Man Up" opportunities (e.g., identifying usage spikes when a starter is sidelined).
* **Optimization Dashboard:** A unified Streamlit/React interface prioritizing "Today's Must-Do Moves."

---

## 🛠️ Technical Stack
* **Language:** Python 3.x
* **Data Processing:** Pandas, NumPy, SciPy (for Z-Score and Variance calculations)
* **API Wrapper:** `espn-api` (Python)
* **Frontend:** Streamlit (for rapid dashboarding) or React.js
* **Data Sources:** ESPN API, Hashtag Basketball (Projections), Underdog NBA (News)

---

## 📊 Core Metrics Defined
| Metric | Purpose |
| :--- | :--- |
| **Z-Score** | Normalizes stats to compare value across different categories (e.g., comparing AST to BLK). |
| **Standard Deviation ($\sigma$)** | Measures scoring consistency; lower $\sigma$ indicates a "reliable" weekly starter. |
| **Variance ($\sigma^2$)** | Analyzes team-wide stability; helps in deciding whether to "swing for upside" in a matchup. |
| **Usage Rate (USG%)** | Predicts volume increases when teammates are injured. |

---

## 🛠️ Installation & Setup
*(Coming Soon - Refer to Phase 1 for Authentication steps)*