import os
from pathlib import Path
import pandas as pd

INPUT_CSV    = Path("gee_data/results_enriched.csv")
OUTPUT_CSV   = Path("gee_data/results_enriched_cleaned.csv")
IMAGES_DIR   = Path("gee_data/images")

KEY_COLS = [
    "temp_mean",
    "precip_sum",
    "wind_mean",
    "cloud_mean",
    "pressure_mean",
    "rh_mean",
    "dewpoint_mean"
]

df = pd.read_csv(INPUT_CSV, sep=";", encoding="cp1250")

# Riadky s chýbajúcimi hodnotami
mask_valid   = df[KEY_COLS].notnull().all(axis=1)
df_invalid   = df[~mask_valid]
df_clean     = df[mask_valid].copy()

# Vymazanie snímok, ktorých riadky boli odstránené
removed = 0
for img_path in df_invalid["image_path"].dropna().unique():
    p = Path(img_path)
    if not p.exists():
        p = IMAGES_DIR / p.name
    if p.exists():
        os.remove(p)
        removed += 1

df_clean.to_csv(OUTPUT_CSV, sep=";", index=False, encoding="cp1250")
