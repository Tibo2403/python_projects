"""Mini pipeline ETL : extraction CSV/JSON -> conversion d'unités -> export CSV."""
import glob
from datetime import datetime

import pandas as pd

COLUMNS = ["name", "height", "weight"]
TARGET_FILE = "transformed_data.csv"
LOG_FILE = "logfile.txt"


def extract_from_csv(file_to_process):
    return pd.read_csv(file_to_process)


def extract_from_json(file_to_process):
    return pd.read_json(file_to_process, lines=True)


def extract():
    frames = [extract_from_csv(f) for f in glob.glob("*.csv") if f != TARGET_FILE]
    frames += [extract_from_json(f) for f in glob.glob("*.json")]
    if not frames:
        return pd.DataFrame(columns=COLUMNS)
    return pd.concat(frames, ignore_index=True)


def transform(data):
    data = data.copy()
    # Pouces -> mètres (1 pouce = 0.0254 m), arrondi à 2 décimales
    data["height"] = (data["height"] * 0.0254).round(2)
    # Livres -> kilogrammes (1 livre = 0.45359237 kg), arrondi à 2 décimales
    data["weight"] = (data["weight"] * 0.45359237).round(2)
    return data


def load(targetfile, data_to_load):
    data_to_load.to_csv(targetfile, index=False)


def log(message):
    timestamp = datetime.now().strftime("%Y-%b-%d-%H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp},{message}\n")


def main():
    log("ETL Job Started")
    log("Extract Job Started")
    extracted_data = extract()
    log("Extract Job Ended")
    log("Transform Job Started")
    transformed_data = transform(extracted_data)
    log("Transform Job Ended")
    log("Load Job Started")
    load(TARGET_FILE, transformed_data)
    log("Load Job Ended")
    log("ETL Job Ended")


if __name__ == "__main__":
    main()
