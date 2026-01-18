
# =========================================
# 04_silver_processing_pandas.py
# Couche SILVER – Nettoyage & Enrichissement
# =========================================

from pymongo import MongoClient
import pandas as pd

# =========================================
# 1. Connexion MongoDB
# =========================================
MONGO_URI = "mongodb+srv://aminatakimbiri:aminatakimbiri25@cluster0.tgepib5.mongodb.net/"

DB_NAME = "urban_mobility"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# =========================================
# 2. Chargement des données Bronze
# =========================================
mobility_data = list(db["mobility_raw"].find({}, {"_id": 0}))
weather_data = list(db["weather_raw"].find({}, {"_id": 0}))
city_data = list(db["city_raw"].find({}, {"_id": 0}))

df_mobility = pd.DataFrame(mobility_data)
df_weather = pd.DataFrame(weather_data)
df_city = pd.DataFrame(city_data)

print("Initial shapes:")
print("Mobility:", df_mobility.shape)
print("Weather :", df_weather.shape)
print("City    :", df_city.shape)

# =========================================
# 3. Conversion des types temporels
# =========================================
df_mobility["start_time"] = pd.to_datetime(df_mobility["start_time"], errors="coerce")
df_mobility["end_time"] = pd.to_datetime(df_mobility["end_time"], errors="coerce")

df_weather["timestamp_hour"] = pd.to_datetime(
    df_weather["timestamp_hour"], errors="coerce"
)

df_city["date"] = pd.to_datetime(df_city["date"], errors="coerce")

# =========================================
# 4. Nettoyage des données (OBLIGATOIRE)
# =========================================

# 4.1 Suppression des doublons
df_mobility = df_mobility.drop_duplicates(
    subset=["station_id", "start_time", "bike_id"]
)

# 4.2 Cohérence temporelle
df_mobility = df_mobility[
    df_mobility["start_time"] < df_mobility["end_time"]
]

# 4.3 Suppression des trajets < 1 minute
df_mobility = df_mobility[df_mobility["duration"] >= 60]

# 4.4 Validation géographique
df_mobility = df_mobility[
    (df_mobility["latitude"].between(-90, 90)) &
    (df_mobility["longitude"].between(-180, 180))
]

# =========================================
# 5. Standardisation
# =========================================

# 5.1 Texte
df_mobility["station_name"] = (
    df_mobility["station_name"]
    .astype(str)
    .str.lower()
    .str.strip()
)

# 5.2 Valeurs manquantes météo
df_weather = df_weather.fillna({
    "precipitation": 0.0,
    "wind_speed": 0.0
})

# =========================================
# 6. Tests de qualité (à documenter)
# =========================================
print("\n--- Data Quality Checks ---")

print("\n% valeurs nulles (mobility):")
print(df_mobility.isnull().mean() * 100)

print("\nDistribution des durées:")
print(df_mobility["duration"].describe())

# =========================================
# 7. Jointures SILVER
# =========================================

# 7.1 Clé temporelle horaire
df_mobility["hour"] = df_mobility["start_time"].dt.floor("H")

# 7.2 Join mobilité ↔ météo (LEFT JOIN)
df_silver = pd.merge(
    df_mobility,
    df_weather,
    left_on="hour",
    right_on="timestamp_hour",
    how="left"
)

# 7.3 Join événements / jours fériés


# Normalisation des dates (sans heure, même type)
df_silver["date_key"] = df_silver["start_time"].dt.strftime("%Y-%m-%d")

# Date city -> string YYYY-MM-DD
df_city["date_key"] = pd.to_datetime(
    df_city["date"], errors="coerce", dayfirst=True
).dt.strftime("%Y-%m-%d")

df_silver = pd.merge(
    df_silver,
    df_city.drop(columns=["date"]),
    on="date_key",
    how="left"
)


print("\nFinal SILVER shape:", df_silver.shape)

# =========================================
# 8. Sauvegarde intermédiaire (optionnelle)
# =========================================
df_silver.to_csv("silver_output.csv", index=False)
print("SILVER layer processing completed successfully.")
