import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# ===============================
# MongoDB Connection
# ===============================
client = MongoClient(
    "mongodb+srv://aminatakimbiri:aminatakimbiri25@cluster0.tgepib5.mongodb.net/"
)

db = client["urban_mobility"]
collection = db["city_raw"]

# ===============================
# Scraping URL
# ===============================
URL = "https://www.calendrier-365.fr/jours-feries.html"
html = requests.get(URL).text
soup = BeautifulSoup(html, "lxml")

# ===============================
# Parse table
# ===============================
rows = soup.find_all("tr")
docs = []

for row in rows[1:]:
    cols = row.find_all("td")
    if len(cols) >= 2:
        docs.append({
            "date": cols[0].text.strip(),
            "event_name": cols[1].text.strip(),
            "event_type": "holiday",
            "is_holiday": True
        })

# ===============================
# Insert into MongoDB
# ===============================
collection.insert_many(docs)
print(f"Inserted {len(docs)} holiday records")
