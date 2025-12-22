import streamlit as st
import pandas as pd
from src.data import espn_connector
from src.utils import config

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
    .metric-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏀 NBA Fantasy H2H Dashboard")

# Sidebar for potentially other controls or generic info
with st.sidebar:
    st.header("League Settings")
    st.write(f"**League ID:** {config.LEAGUE_ID if config.LEAGUE_ID else 'Not Set'}")
    st.write(f"**Season:** {config.SEASON}")
    
    st.info("Ensure .env file is configured with SWID and ESPN_S2 for private leagues.")

# Main Connection Block
if not config.LEAGUE_ID:
    st.warning("Please configure your `.env` file with `LEAGUE_ID`, `SWID`, and `ESPN_S2`.")
else:
    # Try connecting
    with st.spinner("Connecting to ESPN API..."):
        league = espn_connector.get_league_connection()

    if league:
        st.success(f"Connected to League: **{league.settings.name if hasattr(league, 'settings') else 'Unknown League'}**")
        
        # Phase 1: Basic Roster/Team Pulse
        st.subheader("🏆 League Standings & Teams")
        
        teams = league.teams
        if teams:
            # Create a nice dataframe for display
            team_data = []
            for team in teams:
                team_data.append({
                    "Team Name": team.team_name,
                    "Owner": team.owners[0].get('firstName', 'Unknown') if team.owners else 'Unknown',
                    "Wins": team.wins,
                    "Losses": team.losses,
                    "Rank": team.standing
                })
            
            df_teams = pd.DataFrame(team_data)
            st.dataframe(df_teams, use_container_width=True)
            
            st.markdown("---")
            st.subheader("📅 Schedule Tracker (Coming Soon)")
            st.write("Phase 1 - Implementation in progress...")
        else:
            st.write("No teams found. League might be pre-draft or empty.")

    else:
        st.error("Could not retrieve league data. Check your credentials in `.env`.")

