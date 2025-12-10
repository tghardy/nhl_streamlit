import streamlit as st
import nhl_vis_386 as nhl
import pandas as pd

df = nhl.df.copy()


st.title("NHL Explorer")
st.text("Use the sidebar configurations to customize each plot.")

player = st.sidebar.selectbox(
    "Select a player: ",
    options = sorted(df["Player"].unique()),
    index = None
    )

team_map = {t[:3]: t for t in df["Team"].unique()}
team_abbrs = sorted(team_map.keys())

team = st.sidebar.selectbox(
    "Select a team: ",
    options = team_abbrs,
    index = None
)

season = st.sidebar.selectbox(
    "Select a season: ",
    options = sorted(df["Season"].unique()),
    index = None
)

position = st.sidebar.selectbox(
    "Select a position: ",
    options = sorted(df["Pos"].unique()),
    index = None
)

if position is None:
    dfc = df.copy()
else:
    dfc = df[df["Pos"] == position].copy()

x_metric = st.sidebar.selectbox("Select a metric:", options=df.columns, index=list(df.columns).index("G"))
y_metric = st.sidebar.selectbox("Select a metric:", options=df.columns, index=list(df.columns).index("A"))

metrics = [x_metric, y_metric]

fig = nhl.score_scatter(player, season, team, metrics=metrics, df=dfc)
st.plotly_chart(fig, use_container_width=True)
if season is not None and player is not None:
    fig2 = nhl.score_plot(player, season, df=dfc)
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.text("Select a season and player to view plots relative to league average.")


if player is not None:
    aggr = st.toggle("Aggregated:")
    if player is not None:
        if season is not None:
            table1 = nhl.get_player_stats(player, season, aggr, df=dfc)
            table1 = table1[["Player", "Pos", "G", "A", "P", "FOW%", "GP", "PIM", "+/-", "S%", "S/C", "S", "TOI/GP"]]
            st.table(table1)
        else:
            table1 = nhl.get_player_stats(player, aggr=aggr)
            table1 = table1[["Player", "Pos", "G", "A", "P", "FOW%", "GP", "PIM", "+/-", "S%", "S/C", "S", "TOI/GP"]]
            st.table(table1)
else:
    st.text("Select a player to view specific statistics.")


if team is not None and season is not None:
    table2 = nhl.get_roster_stats(team, season)
    table2 = table2[["Player", "Pos", "G", "A", "P", "FOW%", "GP", "PIM", "+/-", "S%", "S/C", "S", "TOI/GP"]]
    st.table(table2)
else:
    st.text("Select a team and season to view roster stats.")
