# Urban Mobility Data Pipeline   

##  Objectif
Construire un pipeline Data Engineering complet pour analyser
la mobilité urbaine des vélos en libre-service en intégrant :
- Données de mobilité (CityBikes)
- Données météorologiques (Open-Meteo)
- Jours fériés (scraping)

##  Architecture
Bronze → Silver → Gold

- **Bronze** : données brutes stockées dans MongoDB
- **Silver** : nettoyage, normalisation, jointures
- **Gold** : agrégations analytiques et stockage Parquet

##  Technologies
- Python
- Pandas
- MongoDB Atlas
- Parquet (pyarrow)

## ▶ Exécution du pipeline
```bash
python run_pipeline.py
