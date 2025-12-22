import streamlit as st
import pandas as pd
import datetime
from src.data import schedule_engine

def render_schedule_analysis(league, matchup_period, week_label, start_date, end_date, my_team=None):
    """
    Renders the schedule analysis for a specific matchup period.
    """
    st.subheader(f"📅 Schedule Analysis: {week_label}")
    
    # Generate daily headers based on the specific range (handling 14-day weeks)
    days_in_range = []
    curr = start_date
    while curr <= end_date:
        days_in_range.append(curr)
        curr += datetime.timedelta(days=1)
        
    day_headers = [d.strftime('%a') for d in days_in_range]
    
    st.caption(f"📅 Analysis Range: **{start_date.strftime('%b %d, %Y')} - {end_date.strftime('%b %d, %Y')}**")
    
    # Import matchup_utils here to avoid circular imports
    from src.data import matchup_utils
    
    # Get matchups from team schedules (more reliable than box_scores for future periods)
    matchup_pairs = matchup_utils.get_matchups_from_team_schedules(league, matchup_period)
    
    if not matchup_pairs:
        st.info(f"No matchups found for Period {matchup_period}.")
        return

    # Sort: My matchup first if team selected
    if my_team:
        matchup_pairs.sort(key=lambda pair: (pair[0].team_id == my_team.team_id or pair[1].team_id == my_team.team_id), reverse=True)

    # Create 3-column layout for compact viewing
    num_columns = 3
    cols = st.columns(num_columns)
    
    # Render MATCHUPS in 3-column grid
    for idx, (home_team, away_team) in enumerate(matchup_pairs):
        col_idx = idx % num_columns
        
        with cols[col_idx]:
            # Identify if this is "My Matchup" for special highlighting
            is_my_matchup = False
            if my_team:
                is_my_matchup = (home_team.team_id == my_team.team_id or away_team.team_id == my_team.team_id)
            
            highlight_border = "border: 2px solid #FF4B4B;" if is_my_matchup else "border: 1px solid #333;"
            
            # Use Streamlit container with custom styling
            with st.container():
                # Add container styling via markdown
                st.markdown("""
                <style>
                .matchup-container {
                    background-color: #0E1117;
                    padding: 10px;
                    border-radius: 12px;
                    margin-bottom: 20px;
                    border: 2px solid #2A2A3A;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                }
                </style>
                <div class="matchup-container">
                """, unsafe_allow_html=True)
                
                # Matchup Card Header (fixed height, centered text)
                st.markdown(f"""
                <div style="background-color: #1E1E1E; padding: 6px; border-radius: 8px; margin-bottom: 12px; {highlight_border} height: 45px; display: flex; align-items: center; justify-content: center;">
                    <div style="margin: 0; text-align: center; font-size: 12px; line-height: 1.2; font-weight: 600;">{home_team.team_name} <span style="color: #aaa; font-size: 0.8em;">vs</span> {away_team.team_name}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Team Stats calculation
                home_total, home_daily = schedule_engine.count_games_in_range(home_team.roster, start_date, end_date)
                away_total, away_daily = schedule_engine.count_games_in_range(away_team.roster, start_date, end_date)
                
                # Home team - side by side layout
                st.markdown(f"""
                <div style="background-color: #1A1A1A; padding: 4px 8px; border-radius: 6px; margin-bottom: 4px; display: flex; align-items: center; justify-content: space-between; height: 35px;">
                    <div style="font-size: 11px; color: #aaa; flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{home_team.team_name}</div>
                    <div style="font-size: 20px; font-weight: bold; color: #FF4B4B; margin-left: 8px;">{home_total}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Away team - side by side layout
                st.markdown(f"""
                <div style="background-color: #1A1A1A; padding: 4px 8px; border-radius: 6px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between; height: 35px;">
                    <div style="font-size: 11px; color: #aaa; flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{away_team.team_name}</div>
                    <div style="font-size: 20px; font-weight: bold; color: #FF4B4B; margin-left: 8px;">{away_total}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Win Probability indicator
                diff = home_total - away_total
                
                # Determine message
                if diff == 0:
                    delta_message = "⚖️ Even"
                    bg_color = "#0D2F4F"
                    border_color = "#1B437A"
                elif diff > 0:
                    delta_message = f"{home_team.team_name} has advantage by {diff}"
                    bg_color = "#0D4F2F"
                    border_color = "#1B7A43"
                else:
                    delta_message = f"{away_team.team_name} has advantage by {abs(diff)}"
                    bg_color = "#4F0D0D"
                    border_color = "#7A1B1B"
                
                st.markdown(f"""
                <div style="background-color: {bg_color}; padding: 6px; border-radius: 6px; text-align: center; border: 1px solid {border_color}; height: 35px; display: flex; align-items: center; justify-content: center; margin-bottom: 8px;">
                    <span style="font-size: 12px;">{delta_message}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Daily breakdown header
                st.markdown("<div style='margin-top: 8px; margin-bottom: 4px; font-size: 11px; color: #aaa; height: 18px;'>📅 Daily Breakdown</div>", unsafe_allow_html=True)
                
                breakdown_data = []
                
                row_home = {"Team": home_team.team_name[:10]}
                row_away = {"Team": away_team.team_name[:10]}
                
                # Iterate through the actual dates in range
                for idx_day, d_obj in enumerate(days_in_range):
                    header = f"{day_headers[idx_day][:3]}"
                    row_home[header] = home_daily[d_obj]
                    row_away[header] = away_daily[d_obj]
                
                breakdown_data.append(row_home)
                breakdown_data.append(row_away)
                
                df_breakdown = pd.DataFrame(breakdown_data)
                st.dataframe(df_breakdown, use_container_width=True, hide_index=True, height=110)
                
                # Close container div
                st.markdown("</div>", unsafe_allow_html=True)
