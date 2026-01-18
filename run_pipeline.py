
# ## ▶️ `run_pipeline.py`

# #Script **orchestrateur** du pipeline 

# # run_pipeline.py

# import subprocess
# import logging
# import os

# LOG_PATH = "logs/pipeline.log"

# logging.basicConfig(
#     filename=LOG_PATH,
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

# def run_script(script_path):
#     logging.info(f"Running {script_path}")
#     result = subprocess.run(
#         ["python", script_path],
#         capture_output=True,
#         text=True
#     )
#     if result.returncode != 0:
#         logging.error(result.stderr)
#         raise RuntimeError(f"Error in {script_path}")
#     logging.info(result.stdout)

# if __name__ == "__main__":
#     logging.info("Pipeline started")

#     run_script("bronze/01_collect_mobility.py")
#     run_script("bronze/02_weather_raw.py")
#     run_script("bronze/03_scrape_holidays.py")
#     run_script("silver/04_silver_processing.py")
#     run_script("gold/05_gold_calculations.py")

#     logging.info("Pipeline finished successfully")


# run_pipeline.py
import subprocess
import logging
import os
import sys

# Base directory du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Chemin vers le fichier de log
LOG_PATH = os.path.join(BASE_DIR, "logs", "pipeline.log")

# Création du dossier logs si nécessaire
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

# Configuration du logging
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_script(script_path):
    script_file = os.path.join(BASE_DIR, script_path)
    logging.info(f"Running {script_file}")
    result = subprocess.run(
        [sys.executable, script_file],
        capture_output=True,
        text=True
    )
    print(result.stdout)  # affiche la sortie standard
    print(result.stderr)  # affiche les erreurs
    if result.returncode != 0:
        logging.error(result.stderr)
        raise RuntimeError(f"Error in {script_path}")
    logging.info(result.stdout)

    if result.returncode != 0:
        logging.error(result.stderr)
        raise RuntimeError(f"Error in {script_path}")
    logging.info(result.stdout)

if __name__ == "__main__":
    logging.info("Pipeline started")

    # Liste des scripts à exécuter dans l'ordre
    scripts = [
        
        "bronze/02_weather_raw.py",
        "bronze/03_scrape_holidays.py",
        "bronze/01_collect_mobility.py",
        "silver/04_silver_processing.py",
        "gold/05_gold_calculations.py",
        "dashboard/app.py",
    ]

    for script in scripts:
        run_script(script)

    logging.info("Pipeline finished successfully")
