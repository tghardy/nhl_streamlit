import streamlit as st
import nhl_vis_386 as nhl
import pandas as pd

# player selectbox

df = nhl.df.copy()

player = st.selectbox(
    "Select a player: ",
    options = sorted(df["Player"].unique()),
    index = None
    )

team_map = {t[:3]: t for t in df["Team"].unique()}
team_abbrs = sorted(team_map.keys())

team = st.selectbox(
    "Select a team: ",
    options = team_abbrs,
    index = None
)

season = st.selectbox(
    "Select a season: ",
    options = sorted(df["Season"].unique()),
    index = None
)

x_metric = st.selectbox("Select a metric:", options=df.columns, index=list(df.columns).index("G"))
y_metric = st.selectbox("Select a metric:", options=df.columns, index=list(df.columns).index("A"))

metrics = [x_metric, y_metric]

fig = nhl.score_scatter(player, season, team, metrics=metrics)
st.plotly_chart(fig, use_container_width=True)
if season is not None:
    fig2 = nhl.score_plot(player, season)
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.text("Select a season and player to view plots relative to league average.")