# # =========================================
# # 05_gold_calculations.py
# # Couche GOLD – Analytics & Parquet
# # =========================================

# import pandas as pd
# import numpy as np
# from math import radians, cos, sin, asin, sqrt

# # =========================================
# # 1. Charger la couche SILVER
# # =========================================
# df = pd.read_csv("silver_output.csv", parse_dates=["start_time", "end_time"])

# print("SILVER loaded:", df.shape)

# # =========================================
# # 2. INDICATEUR RUSH HOUR (OBLIGATOIRE)
# # =========================================

# df["hour_of_day"] = df["start_time"].dt.hour

# df["is_rush_hour"] = np.where(
#     ((df["hour_of_day"].between(7, 9)) |
#      (df["hour_of_day"].between(17, 19))),
#     1,
#     0
# )

# # =========================================
# # 3. CATÉGORISATION DE LA DURÉE (QUANTILES)
# # =========================================

# q1 = df["duration"].quantile(0.33)
# q2 = df["duration"].quantile(0.66)

# def duration_category(d):
#     if d <= q1:
#         return "short"
#     elif d <= q2:
#         return "medium"
#     else:
#         return "long"

# df["duration_category"] = df["duration"].apply(duration_category)

# # =========================================
# # 4. MÉTÉO IMPACT SCORE
# # =========================================

# weather_impact = (
#     df.groupby("condition")["duration"]
#     .mean()
#     .reset_index()
#     .rename(columns={"duration": "avg_duration"})
# )

# df = df.merge(weather_impact, on="condition", how="left")
# df.rename(columns={"avg_duration": "weather_impact_score"}, inplace=True)

# # =========================================
# # 5. DISTANCE LINÉAIRE (HAVERSINE)
# # =========================================

# def haversine(lat, lon):
#     R = 6371  # km
#     lat, lon = radians(lat), radians(lon)
#     return 2 * R * asin(sqrt(
#         sin(lat / 2) ** 2 + cos(lat) * sin(lon / 2) ** 2
#     ))

# df["distance_km"] = df.apply(
#     lambda row: haversine(row["latitude"], row["longitude"]),
#     axis=1
# )

# # =========================================
# # 6. TAUX DE CROISSANCE JOURNALIER
# # =========================================

# df["date"] = df["start_time"].dt.date

# daily_volume = (
#     df.groupby(["station_id", "date"])
#     .size()
#     .reset_index(name="daily_trips")
# )

# daily_volume["rolling_7d_avg"] = (
#     daily_volume.groupby("station_id")["daily_trips"]
#     .transform(lambda x: x.rolling(7, min_periods=1).mean())
# )

# daily_volume["growth_rate"] = (
#     (daily_volume["daily_trips"] - daily_volume["rolling_7d_avg"])
#     / daily_volume["rolling_7d_avg"]
# )

# df = df.merge(
#     daily_volume[["station_id", "date", "growth_rate"]],
#     on=["station_id", "date"],
#     how="left"
# )

# # =========================================
# # 7. PARTITIONNEMENT TEMPOREL
# # =========================================

# df["year"] = df["start_time"].dt.year
# df["month"] = df["start_time"].dt.month
# df["day"] = df["start_time"].dt.day

# # =========================================
# # 8. ÉCRITURE PARQUET (GOLD)
# # =========================================

# df.to_parquet(
#     "gold/gold_data/",
#     partition_cols=["year", "month", "day"],
#     index=False
# )

# print("GOLD layer written successfully (Parquet partitioned)")
# print("Final GOLD shape:", df.shape)


# =========================================
# 05_gold_calculations.py
# Couche GOLD – Analytics & Dashboard Ready
# =========================================

import pandas as pd
import numpy as np
import os

os.makedirs("gold", exist_ok=True)

# =========================================
# 1. Charger la couche SILVER
# =========================================
df = pd.read_csv(
    "silver_output.csv",
    parse_dates=["start_time", "end_time"]
)

print("SILVER loaded:", df.shape)

# =========================================
# 2. INDICATEUR RUSH HOUR
# =========================================
df["hour_of_day"] = df["start_time"].dt.hour

df["is_rush_hour"] = np.where(
    ((df["hour_of_day"].between(7, 9)) |
     (df["hour_of_day"].between(17, 19))),
    1, 0
)

# =========================================
# 3. CATÉGORIE DE DURÉE
# =========================================
q1 = df["duration"].quantile(0.33)
q2 = df["duration"].quantile(0.66)

df["duration_category"] = pd.cut(
    df["duration"],
    bins=[0, q1, q2, df["duration"].max()],
    labels=["short", "medium", "long"]
)

# =========================================
# 4. WEATHER IMPACT SCORE
# =========================================
weather_impact = (
    df.groupby("condition")["duration"]
    .mean()
    .reset_index(name="weather_impact_score")
)

df = df.merge(weather_impact, on="condition", how="left")

# =========================================
# 5. TAUX DE CROISSANCE JOURNALIER
# =========================================
df["date"] = df["start_time"].dt.date

daily = (
    df.groupby(["station_id", "date"])
    .size()
    .reset_index(name="daily_trips")
)

daily["rolling_7d_avg"] = (
    daily.groupby("station_id")["daily_trips"]
    .transform(lambda x: x.rolling(7, min_periods=1).mean())
)

daily["growth_rate"] = (
    (daily["daily_trips"] - daily["rolling_7d_avg"])
    / daily["rolling_7d_avg"]
)

df = df.merge(
    daily[["station_id", "date", "growth_rate"]],
    on=["station_id", "date"],
    how="left"
)

# =========================================
# 6. ÉCRITURE GOLD (UN SEUL PARQUET)
# =========================================
output_path = "gold/mobility_gold.parquet"

df.to_parquet(
    output_path,
    engine="pyarrow",
    index=False
)

print("GOLD written:", output_path)
print("Final GOLD shape:", df.shape)
