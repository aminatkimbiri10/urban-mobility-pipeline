
# from pymongo import MongoClient

# uri = "mongodb+srv://aminatakimbiri:aminatakimbiri25@cluster0.tgepib5.mongodb.net/"
# client = MongoClient(uri, serverSelectionTimeoutMS=5000)

# try:
#     print(client.server_info())
#     print("✅ Connected to MongoDB")
# except Exception as e:
#     print("❌ Connection failed")
#     print(e)

from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://aminatakimbiri:aminatakimbiri25@cluster0.tgepib5.mongodb.net/"
)

db = client["urban_mobility"]
mobility_col = db["mobility_raw"]
weather_col = db["weather_raw"]
city_col = db["city_raw"]

