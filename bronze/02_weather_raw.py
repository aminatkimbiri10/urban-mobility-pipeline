# import requests
# from pymongo import MongoClient

# # ===============================
# # MongoDB Connection
# # ===============================
# client = MongoClient(
#     "mongodb+srv://aminatakimbiri:aminatakimbiri25@cluster0.tgepib5.mongodb.net/"
# )

# db = client["urban_mobility"]
# collection = db["weather_raw"]

# # ===============================
# # Open-Meteo API (Paris)
# # ===============================
# URL = (
#     "https://api.open-meteo.com/v1/forecast?"
#     "latitude=48.8566&longitude=2.3522"
#     "&hourly=temperature_2m,precipitation,wind_speed_10m"
#     "&timezone=Europe/Paris"
# )

# data = requests.get(URL).json()["hourly"]

# # ===============================
# # Transformation
# # ===============================
# docs = []
# for i in range(len(data["time"])):
#     precipitation = data["precipitation"][i]
#     wind = data["wind_speed_10m"][i]

#     if precipitation > 5:
#         condition = "rain"
#     elif wind > 20:
#         condition = "windy"
#     else:
#         condition = "clear"

#     docs.append({
#         "timestamp_hour": data["time"][i],
#         "temperature_C": data["temperature_2m"][i],
#         "wind_speed": wind,
#         "precipitation": precipitation,
#         "condition": condition
#     })

# # ===============================
# # Insert into MongoDB
# # ===============================
# collection.insert_many(docs)
# print(f"Inserted {len(docs)} weather records")


import requests
from pymongo import MongoClient


# ===============================
# MongoDB Connection
# ===============================
client = MongoClient(
    "mongodb+srv://aminatakimbiri:aminatakimbiri25@cluster0.tgepib5.mongodb.net/"
)
db = client["urban_mobility"]
collection = db["weather_raw"]



# ===============================
# Open-Meteo API (Paris)
# ===============================
URL = (
    "https://api.open-meteo.com/v1/forecast?"
    "latitude=48.8566&longitude=2.3522"
    "&hourly=temperature_2m,precipitation,wind_speed_10m"
    "&timezone=Europe/Paris"
)

data = requests.get(URL).json()["hourly"]

# ===============================
# Transformation
# ===============================
docs = []
for i in range(len(data["time"])):
    precipitation = data["precipitation"][i]
    wind = data["wind_speed_10m"][i]

    if precipitation > 5:
        condition = "rain"
    elif wind > 20:
        condition = "windy"
    else:
        condition = "clear"

    docs.append({
        "timestamp_hour": data["time"][i],
        "temperature_C": data["temperature_2m"][i],
        "wind_speed": wind,
        "precipitation": precipitation,
        "condition": condition
    })

# ===============================
# Insert into MongoDB
# ===============================
collection.insert_many(docs)
print(f"Inserted {len(docs)} weather records")
