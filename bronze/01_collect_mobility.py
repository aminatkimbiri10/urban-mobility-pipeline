import requests
import random
from datetime import datetime, timedelta
from pymongo import MongoClient

# ===============================
# MongoDB Connection
# ===============================
client = MongoClient(
    "mongodb+srv://aminatakimbiri:aminatakimbiri25@cluster0.tgepib5.mongodb.net/"
)

db = client["urban_mobility"]
collection = db["mobility_raw"]

# ===============================
# CityBikes API
# ===============================
API_URL = "https://api.citybik.es/v2/networks/velib"
response = requests.get(API_URL)
stations = response.json()["network"]["stations"]

# ===============================
# Generate simulated trips
# ===============================
base_date = datetime(2024, 1, 1)
docs = []

for day in range(18):          # 30 jours
    for station in stations:
        for _ in range(20):    # volume par station
            start_time = base_date + timedelta(
                days=day,
                minutes=random.randint(0, 1440)
            )
            duration = random.randint(60, 3600)

            docs.append({
                "station_id": station["id"],
                "station_name": station["name"],
                "bike_id": f"bike_{random.randint(1, 10000)}",
                "start_time": start_time,
                "end_time": start_time + timedelta(seconds=duration),
                "duration": duration,
                "latitude": station["latitude"],
                "longitude": station["longitude"]
            })

# ===============================
# Insert into MongoDB
# ===============================
collection.insert_many(docs)
print(f"Inserted {len(docs)} mobility records")
