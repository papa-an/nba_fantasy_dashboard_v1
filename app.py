import streamlit as st
import pandas as pd
from src.data import espn_connector, news_aggregator, schedule_engine, matchup_calendar
from src.analysis import roster_analyzer
from src.ui import schedule_view
from src.utils import config
import datetime

# Page Configuration
st.set_page_config(
    page_title="NBA Fantasy Dashboard",
    page_icon="🏀",
    layout="wide"
)

# Custom CSS for aesthetics (Phase 1 Foundation)
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
        color: #FF4B4B;
    }
    .news-card {
        background-color: #262730;
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 8px;
        border-left: 4px solid #FF4B4B;
    }
    .news-headline {
        font-size: 16px;
        font-weight: bold;
        color: #fff;
        margin-bottom: 5px;
    }
    .news-meta {
        font-size: 12px;
        color: #aaa;
        margin-bottom: 10px;
    }
    .news-report {
        font-size: 14px;
        color: #ddd;
    }
    .vs-card {
        background-color: #0E1117;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #333;
    }
    .vs-score {
        font-size: 24px; 
        font-weight: bold; 
        color: #FF4B4B;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏀 NBA Fantasy H2H Dashboard")

# Initialize Session State for Team Selection
if 'my_team_idx' not in st.session_state:
    st.session_state.my_team_idx = 0

# Sidebar
with st.sidebar:
    st.header("League Settings")
    st.write(f"**League ID:** {config.LEAGUE_ID if config.LEAGUE_ID else 'Not Set'}")
    st.write(f"**Season:** {config.SEASON}")
    

# Main Connection Block
if not config.LEAGUE_ID:
    st.warning("Please configure your `.env` file with `LEAGUE_ID`, `SWID`, and `ESPN_S2`.")
else:
    # Try connecting
    with st.spinner("Connecting to ESPN API..."):
        league = espn_connector.get_league_connection()

    if league:
        # NOTE: The name "PERMAI LEAGUE 2025" comes directly from ESPN settings, not our code!
        st.success(f"Connected to **{league.settings.name}** (Season {config.SEASON})")
        
        # --- Team Selector (Moved here to use league data) ---
        team_names = [team.team_name for team in league.teams]
        selected_team_name = st.sidebar.selectbox("Select Your Team", team_names, index=st.session_state.my_team_idx)
        
        # Find the actual team object
        my_team = next((t for t in league.teams if t.team_name == selected_team_name), None)
        # Update session state index (optional, for persist)
        if my_team:
             st.session_state.my_team_idx = team_names.index(selected_team_name)
        # -----------------------------------------------------

        # Tabs for Phase 1 & 2 Features
        tab1, tab_strat, tab2, tab3, tab4 = st.tabs([
            "🏆 Standings", 
            "🏛️ Strategy Room",
            "📰 Player News", 
            "📅 Current Week", 
            "🔮 Upcoming Week"
        ])
        
        with tab1:
            st.subheader("League Standings")
            teams = league.teams
            if teams:
                # Create a nice dataframe for display
                team_data = []
                for team in teams:
                    total_games = team.wins + team.losses + team.ties
                    win_pct = team.wins / total_games if total_games > 0 else 0.0
                    
                    team_data.append({
                        "Team Name": team.team_name,
                        "Owner": team.owners[0].get('firstName', 'Unknown') if team.owners else 'Unknown',
                        "Wins": team.wins,
                        "Losses": team.losses,
                        "Ties": team.ties,
                        "Win %": f"{win_pct:.3f}",
                        "Rank": team.standing
                    })
                
                df_teams = pd.DataFrame(team_data)
                st.dataframe(df_teams, use_container_width=True, hide_index=True)
            else:
                st.write("No teams found.")

        with tab_strat:
            st.header("🏛️ Strategy Room")
            st.info("📊 **Phase 2 Implementation Started:** Statistical Engine Calibration in progress.")
            
            # Variable to store insights
            roster_insights = None
            
            # Layout: Left side for Heatmap (Placeholder), Right side for Team DNA
            col_heatmap, col_dna = st.columns([3, 2])
            
            with col_heatmap:
                st.subheader("League Power Matrix")
                # Visual Placeholder for Heatmap
                st.markdown("""
                <div style="background-color: #1E1E1E; padding: 40px; border-radius: 10px; border: 1px dashed #444; text-align: center;">
                    <div style="font-size: 40px;">🧪</div>
                    <div style="font-size: 16px; font-weight: bold; margin-top: 10px;">9-Cat Z-Score Heatmap coming in Phase 2</div>
                    <div style="font-size: 12px; color: #888;">Calibrating League Medians...</div>
                </div>
                """, unsafe_allow_html=True)

            with col_dna:
                st.subheader("Roster DNA")
                # Specific Team Selector for this tab
                target_team_name = st.selectbox(
                    "Select Team to Analyze", 
                    team_names, 
                    index=st.session_state.my_team_idx,
                    key="strat_team_select"
                )
                
                target_team = next((t for t in league.teams if t.team_name == target_team_name), None)
                
                if target_team:
                    roster_data = []
                    for player in target_team.roster:
                        # Extract basic info
                        roster_data.append({
                            "Player": player.name,
                            "POS": player.position,
                            "Status": "✅ Active" if player.injuryStatus == "ACTIVE" else f"🚑 {player.injuryStatus}",
                            "Acquired": player.acquisitionType
                        })
                    
                    df_roster = pd.DataFrame(roster_data)
                    st.dataframe(df_roster, use_container_width=True, hide_index=True)
                    
                    # Compute insights for display below
                    roster_insights = roster_analyzer.generate_roster_insight(target_team.roster)
                    
                else:
                    st.write("Select a team to see roster DNA.")

            # Full-Width AI Insights Section
            if roster_insights:
                st.markdown("---")
                st.subheader("🤖 AI-Generated Insights")
                
                col_i1, col_i2, col_i3 = st.columns(3)
                
                # 1. Roster Composition (Red Theme)
                with col_i1:
                    st.markdown(f"""
                    <div style="background-color: #262730; padding: 15px; border-radius: 8px; border-top: 4px solid #FF4B4B; min-height: 180px;">
                        <div style="font-weight: bold; color: #FF4B4B; margin-bottom: 8px;">📊 Roster Composition</div>
                        <div style="font-size: 13px; color: #ddd; line-height: 1.4;">
                            {roster_insights['composition_report']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                # 2. How to Win (Green Theme)
                with col_i2:
                    st.markdown(f"""
                    <div style="background-color: #262730; padding: 15px; border-radius: 8px; border-top: 4px solid #00CC66; min-height: 180px;">
                        <div style="font-weight: bold; color: #00CC66; margin-bottom: 8px;">🏆 How to Win</div>
                        <div style="font-size: 13px; color: #ddd; line-height: 1.4;">
                            {roster_insights['win_strategy']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                # 3. How to Improve (Blue Theme)
                with col_i3:
                    st.markdown(f"""
                    <div style="background-color: #262730; padding: 15px; border-radius: 8px; border-top: 4px solid #3399FF; min-height: 180px;">
                        <div style="font-weight: bold; color: #3399FF; margin-bottom: 8px;">💡 How to Improve</div>
                        <div style="font-size: 13px; color: #ddd; line-height: 1.4;">
                            {roster_insights['improvement_plan']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            st.divider()
            st.subheader("🎯 Smart Waiver Radar")
            st.caption("Identifying high-value category streamers based on weighted Z-Scores...")
            st.markdown("""
            <div style="background-color: #0E1117; padding: 15px; border-radius: 8px; border: 1px solid #333;">
                <i>Foundation being built for category-specific re-ranking.</i>
            </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.subheader("🔥 Latest Player News")
            if st.button("Refresh News", key='news_refresh'):
                st.rerun()
                
            with st.spinner("Fetching latest news..."):
                # Filter Logic (Basic)
                news_items = news_aggregator.fetch_player_news()
                
                # If my_team is selected, we could filter here. 
                # For now, let's just show all but highlight 'My Players' maybe?
                # User asked to just build Schedule Tracker now, so keeping this simple.
                
            if news_items:
                for item in news_items:
                    # Check if player is on my roster
                    is_my_player = False
                    if my_team:
                        # Simple substring match (API name vs News name can differ slightly)
                        is_my_player = any(p.name in item['player'] or item['player'] in p.name for p in my_team.roster)
                    
                    highlight_style = "border-left: 4px solid #00FF00;" if is_my_player else ""
                    
                    # Using Custom HTML for News Cards
                    player_team = f"{item['player']} - {item['team']}" if item['team'] else item['player']
                    st.markdown(f"""
                    <div class="news-card" style="{highlight_style}">
                        <div class="news-headline">{player_team} {'🟢 MY TEAM' if is_my_player else ''}</div>
                        <div class="news-meta">{item['date']}</div>
                        <div class="news-report">{item['headline']}</div>
                        <hr style="border-color: #444; margin: 8px 0;">
                        <div class="news-report" style="font-style: italic; opacity: 0.8;">{item['report']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No news found or connection error.")
        
        with tab3:
            # Current Week Analysis
            # 1. Determine Correct Matchup Period & Dates
            #   We trust our Calculated Calendar more than determining "Dates by simple Offset"
            #   But we trust "league.currentMatchupPeriod" for the "Active Box Scores".
            
            # Since the API seems slightly off/laggy on M9 vs M10, let's use Date-Based lookup
            # Calculate Schedule Map
            schedule_map = matchup_calendar.get_matchup_schedule(season_year=config.SEASON)
            
            # Find ID for today
            today = datetime.date.today()
            current_matchup_id = matchup_calendar.get_current_matchup_period_id(schedule_map, today)
            
            # Get Dates for THIS ID
            start_date, end_date = schedule_map[current_matchup_id]
            
            schedule_view.render_schedule_analysis(
                league=league,
                matchup_period=current_matchup_id, 
                week_label=f"Matchup {current_matchup_id} (Current Week)",
                start_date=start_date,
                end_date=end_date,
                my_team=my_team
            )

        with tab4:
            # Upcoming Week Analysis
            # Next ID
            next_matchup_id = current_matchup_id + 1
            if next_matchup_id in schedule_map:
                start_date_next, end_date_next = schedule_map[next_matchup_id]
                
                schedule_view.render_schedule_analysis(
                    league=league,
                    matchup_period=next_matchup_id,
                    week_label=f"Matchup {next_matchup_id} (Next Week)",
                    start_date=start_date_next,
                    end_date=end_date_next,
                    my_team=my_team
                )
            else:
                st.info("No upcoming matchup found in schedule.")


            


    else:
        st.error("Could not retrieve league data. Check your credentials in `.env`.")

