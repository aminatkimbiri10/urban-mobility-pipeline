# # import streamlit as st
# # import pandas as pd
# # import plotly.express as px
# # from datetime import datetime
# # from streamlit_autorefresh import st_autorefresh

# # st.set_page_config(
# #     page_title="Urban Mobility Dashboard",
# #     layout="wide"
# # )

# # st.title("🚲 Urban Mobility – Real-Time Dashboard")

# # # Auto refresh
# # st_autorefresh(interval=60_000, key="refresh")



# # # Load GOLD data
# # df = pd.read_parquet("gold/mobility_gold.parquet")

# # # KPIs
# # col1, col2, col3, col4, col5 = st.columns(5)

# # col1.metric("🚲 Total Trajets", f"{len(df):,}")
# # col2.metric("⏱️ Durée Moyenne (min)", round(df["duration"].mean() / 60, 2))
# # #col3.metric("🌡️ Température Moy.", round(df["temperature"].mean(), 1))
# # weather_score = df["weather_impact_score"].dropna().mean()
# # col3.metric(
# #     "🌦️ Weather Impact Score",
# #     round(weather_score, 1) if not pd.isna(weather_score) else "N/A"
# # )

# # col4.metric("📅 % Jours fériés",
# #             round(df["is_holiday"].mean() * 100, 2))
# # col5.metric(
# #     "⌛ Heure la + active",
# #     df["hour"].mode()[0]
# # )


# # st.divider()

# # # Charts
# # fig_hour = px.line(
# #     df.groupby("hour").size().reset_index(name="trips"),
# #     x="hour",
# #     y="trips",
# #     title="Trajets par Heure"
# # )

# # fig_day = px.bar(
# #     df.groupby("date").size().reset_index(name="trips"),
# #     x="date",
# #     y="trips",
# #     title="Trajets par Jour"
# # )


# # fig_weather = px.scatter(
# #     df,
# #     x="temperature_C",
# #     y="duration",
# #     title="Impact de la Température sur la Durée des Trajets (°C)"
# # )


# # st.plotly_chart(fig_hour, use_container_width=True)
# # st.plotly_chart(fig_day, use_container_width=True)
# # st.plotly_chart(fig_weather, use_container_width=True)


# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from streamlit_autorefresh import st_autorefresh

# # =====================================================
# # CONFIGURATION GLOBALE
# # =====================================================
# st.set_page_config(
#     page_title="Urban Mobility Dashboard",
#     layout="wide"
# )

# st.title("🚲 Urban Mobility – Real-Time Dashboard")

# # Auto refresh (60s)
# st_autorefresh(interval=60_000, key="refresh")

# # =====================================================
# # CHARGEMENT DES DONNÉES
# # =====================================================
# @st.cache_data
# def load_data():
#     df = pd.read_parquet("gold/mobility_gold.parquet")
#     df["is_holiday"] = df["is_holiday"].fillna(0).astype(int)
#     return df

# df = load_data()

# # =====================================================
# # SIDEBAR – FILTRES INTERACTIFS
# # =====================================================
# st.sidebar.header("🎛️ Filtres")

# # Filtre date
# date_min = df["date"].min()
# date_max = df["date"].max()
# date_range = st.sidebar.date_input(
#     "📅 Période",
#     value=(date_min, date_max),
#     min_value=date_min,
#     max_value=date_max
# )

# # Filtre station
# stations = st.sidebar.multiselect(
#     "🚏 Station",
#     options=df["station_name"].unique(),
#     default=df["station_name"].unique()
# )

# # Filtre rush hour
# rush_filter = st.sidebar.selectbox(
#     "⏰ Rush Hour",
#     options=["Tous", "Rush Hour uniquement", "Hors Rush Hour"]
# )

# # =====================================================
# # APPLICATION DES FILTRES
# # =====================================================
# df_filtered = df[
#     (df["date"] >= date_range[0]) &
#     (df["date"] <= date_range[1]) &
#     (df["station_name"].isin(stations))
# ]

# if rush_filter == "Rush Hour uniquement":
#     df_filtered = df_filtered[df_filtered["is_rush_hour"] == 1]
# elif rush_filter == "Hors Rush Hour":
#     df_filtered = df_filtered[df_filtered["is_rush_hour"] == 0]

# # =====================================================
# # KPIs (TOUJOURS EN HAUT)
# # =====================================================
# st.subheader("📊 Indicateurs Clés de Performance")

# col1, col2, col3, col4, col5 = st.columns(5)

# col1.metric("🚲 Total Trajets", f"{len(df_filtered):,}")

# col2.metric(
#     "⏱️ Durée Moyenne (min)",
#     round(df_filtered["duration"].mean() / 60, 2)
# )

# weather_score = df_filtered["weather_impact_score"].dropna().mean()
# col3.metric(
#     "🌦️ Weather Impact Score",
#     round(weather_score, 1) if not pd.isna(weather_score) else "N/A"
# )

# col4.metric(
#     "📅 % Jours fériés",
#     round(df_filtered["is_holiday"].mean() * 100, 2)
# )

# col5.metric(
#     "⌛ Heure la + active",
#     f"{int(df_filtered['hour_of_day'].mode()[0])} h"
# )

# st.divider()

# # =====================================================
# # GRAPHIQUES – LIGNE 1
# # =====================================================
# st.subheader("📈 Analyse Temporelle")

# colA, colB = st.columns(2)

# with colA:
#     fig_hour = px.line(
#         df_filtered.groupby("hour_of_day").size().reset_index(name="trips"),
#         x="hour_of_day",
#         y="trips",
#         markers=True,
#         title="Trajets par Heure"
#     )
#     st.plotly_chart(fig_hour, use_container_width=True)

# with colB:
#     fig_day = px.bar(
#         df_filtered.groupby("date").size().reset_index(name="trips"),
#         x="date",
#         y="trips",
#         title="Trajets par Jour"
#     )
#     st.plotly_chart(fig_day, use_container_width=True)

# # =====================================================
# # GRAPHIQUES – LIGNE 2
# # =====================================================
# st.subheader("🌦️ Impact des Facteurs Externes")

# colC, colD = st.columns(2)

# with colC:
#     fig_weather = px.scatter(
#         df_filtered,
#         x="temperature_C",
#         y="duration",
#         opacity=0.4,
#         title="Température vs Durée des Trajets (°C)"
#     )
#     st.plotly_chart(fig_weather, use_container_width=True)

# with colD:
#     fig_rush = px.box(
#         df_filtered,
#         x="is_rush_hour",
#         y="duration",
#         labels={"is_rush_hour": "Rush Hour"},
#         title="Durée des Trajets – Rush vs Hors Rush"
#     )
#     st.plotly_chart(fig_rush, use_container_width=True)

# # =====================================================
# # FOOTER
# # =====================================================
# st.caption("📌 Données mises à jour automatiquement – Pipeline Urban Mobility")

# =========================================
# Urban Mobility Dashboard - Streamlit
# =========================================

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
import folium
from streamlit_folium import st_folium

# =========================================
# CONFIG
# =========================================
st.set_page_config(
    page_title="Urban Mobility Dashboard",
    layout="wide"
)

st.title("🚲 Urban Mobility – Real-Time Dashboard")

# Auto refresh every 60 seconds
st_autorefresh(interval=60_000, key="refresh")

# =========================================
# LOAD DATA (GOLD)
# =========================================
@st.cache_data
def load_data():
    return pd.read_parquet("gold/mobility_gold.parquet")

df = load_data()

# Ensure datetime
df["start_time"] = pd.to_datetime(df["start_time"])

# =========================================
# SIDEBAR FILTERS
# =========================================
st.sidebar.header("🎛️ Filtres")

date_range = st.sidebar.date_input(
    "📅 Période",
    [df["start_time"].min().date(), df["start_time"].max().date()]
)

station_filter = st.sidebar.multiselect(
    "🚏 Station",
    options=df["station_name"].unique()
)

rush_filter = st.sidebar.selectbox(
    "⏰ Rush Hour",
    ["Tous", "Oui", "Non"]
)

# =========================================
# APPLY FILTERS
# =========================================
df_filtered = df[
    (df["start_time"].dt.date >= date_range[0]) &
    (df["start_time"].dt.date <= date_range[1])
]

if station_filter:
    df_filtered = df_filtered[df_filtered["station_name"].isin(station_filter)]

if rush_filter == "Oui":
    df_filtered = df_filtered[df_filtered["is_rush_hour"] == 1]
elif rush_filter == "Non":
    df_filtered = df_filtered[df_filtered["is_rush_hour"] == 0]

# =========================================
# KPIs
# =========================================
st.subheader("📊 Indicateurs Clés")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("🚲 Total Trajets", f"{len(df_filtered):,}")
col2.metric("⏱️ Durée Moyenne (min)", round(df_filtered["duration"].mean() / 60, 2))

weather_score = df_filtered["weather_impact_score"].dropna().mean()
col3.metric(
    "🌦️ Weather Impact Score",
    round(weather_score, 2) if not pd.isna(weather_score) else "N/A"
)

col4.metric(
    "📅 % Jours fériés",
    round(df_filtered["is_holiday"].mean() * 100, 2)
)

col5.metric(
    "⌛ Heure la + active",
    int(df_filtered["hour_of_day"].mode()[0])
)

st.divider()

# =========================================
# TEMPORAL ANALYSIS (ROW 1)
# =========================================
col1, col2 = st.columns(2)

fig_hour = px.line(
    df_filtered.groupby("hour_of_day").size().reset_index(name="trips"),
    x="hour_of_day",
    y="trips",
    title="Trajets par Heure",
    markers=True
)

fig_day = px.bar(
    df_filtered.groupby("date").size().reset_index(name="trips"),
    x="date",
    y="trips",
    title="Trajets par Jour"
)

col1.plotly_chart(fig_hour, use_container_width=True)
col2.plotly_chart(fig_day, use_container_width=True)

# =========================================
# WEATHER & DURATION (ROW 2)
# =========================================
col1, col2 = st.columns(2)

fig_weather = px.scatter(
    df_filtered,
    x="temperature_C",
    y="duration",
    title="Impact de la Température sur la Durée des Trajets",
    opacity=0.4
)

fig_duration = px.box(
    df_filtered,
    x="duration_category",
    y="duration",
    title="Durée des Trajets par Catégorie"
)

col1.plotly_chart(fig_weather, use_container_width=True)
col2.plotly_chart(fig_duration, use_container_width=True)

# =========================================
# HEATMAP HEURE × JOUR
# =========================================
st.subheader("🔥 Intensité des Trajets (Heure × Jour)")

df_filtered["day_of_week"] = df_filtered["start_time"].dt.day_name()

heatmap_data = (
    df_filtered
    .groupby(["day_of_week", "hour_of_day"])
    .size()
    .reset_index(name="trips")
)

days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

heatmap_data["day_of_week"] = pd.Categorical(
    heatmap_data["day_of_week"],
    categories=days_order,
    ordered=True
)

fig_heatmap = px.density_heatmap(
    heatmap_data,
    x="hour_of_day",
    y="day_of_week",
    z="trips",
    color_continuous_scale="Viridis"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# =========================================
# MAP – STATIONS
# =========================================
st.subheader("🗺️ Carte Interactive des Stations")

station_map = folium.Map(
    location=[df_filtered["latitude"].mean(), df_filtered["longitude"].mean()],
    zoom_start=13
)

stations_grouped = (
    df_filtered
    .groupby(["station_name", "latitude", "longitude"])
    .size()
    .reset_index(name="trips")
)

for _, row in stations_grouped.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=min(row["trips"] / 50, 15),
        popup=f"{row['station_name']}<br>Trajets: {row['trips']}",
        color="blue",
        fill=True,
        fill_opacity=0.6
    ).add_to(station_map)

st_folium(station_map, width=1100, height=500)

# =========================================
# FOOTER
# =========================================
st.markdown("---")
st.caption("📌 Urban Mobility Data Pipeline – GOLD Layer Dashboard")
