import os
import shutil
import pandas as pd
import numpy as np
from PIL import Image
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

INPUT_CSV       = Path("dataset_numerical_binary.csv")
OUTPUT_CSV      = Path("dataset_filtered.csv")        

IMAGES_DIR      = Path("sentinel_data")
BACKUP_DIR      = Path("removed_images") 

CLOUD_META_TH   = 10.0    # Maximálne povolené % oblačnosti v metadátach
WHITENESS_PX_TH = 190     # Prahová hodnota pre jas pixelu
WHITENESS_PCT   = 5.0     # Maximálne povolené % bielych pixelov
BRIGHTNESS_TH   = 160.0   # Maximálny povolený priemerný jas fotky
BLACK_PCT_TH    = 10.0    # Maximálne povolené % čiernych pixelov
MAX_WORKERS     = 8       # Počet vlákien

BACKUP_DIR.mkdir(parents=True, exist_ok=True)

# Analýza obrázka
def analyze_image_quality(row_data):
    """
    Vstup: (index, image_path_str, cloud_percentage)
    Výstup: (index, status, reason)
    """
    idx, img_path_str, cloud_meta = row_data
    img_path = Path(img_path_str)
    
    if not img_path.exists():
        return idx, "missing", "File not found"

    if cloud_meta > CLOUD_META_TH:
        return idx, "bad", f"Oblačnosť gt {CLOUD_META_TH}%"

    # Analýza Pixelov
    try:
        with Image.open(img_path) as img:
            arr = np.array(img.convert("RGB"))
            total_px = arr.shape[0] * arr.shape[1]

            # Čierne pixely
            black_px = np.sum(np.all(arr == 0, axis=2))
            black_pct = (black_px / total_px) * 100.0
            if black_pct > BLACK_PCT_TH:
                return idx, "bad", f"Čierne pixely {black_pct:.1f}%"

            # Príliš jasné snímky
            avg_brightness = np.mean(arr)
            if avg_brightness > BRIGHTNESS_TH:
                return idx, "bad", f"Moc jasné {avg_brightness:.1f}"

            # Biele pixely
            white_mask = np.all(arr > WHITENESS_PX_TH, axis=2)
            white_px = np.sum(white_mask)
            white_pct = (white_px / total_px) * 100.0

            if white_pct > WHITENESS_PCT:
                return idx, "bad", f"Príliš biele {white_pct:.1f}%"

            return idx, "good", "OK"

    except Exception as e:
        return idx, "error", str(e)

def main():

    df = pd.read_csv(INPUT_CSV, sep=';', encoding="cp1250")

    # Príprava dát pre threading
    work_items = list(zip(df.index, df['image_path'], df['cloud_percentage'].fillna(0)))

    results_map = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = list(tqdm(executor.map(analyze_image_quality, work_items), total=len(work_items)))

    for res in results:
        results_map[res[0]] = (res[1], res[2])

    # Čistenie, presúvanie a triedenie
    indices_to_keep = []
    stats = {"missing": 0, "bad": 0, "error": 0, "good": 0}

    for idx in df.index:
        status, reason = results_map.get(idx, ("error", "Unknown"))
        img_path = Path(df.loc[idx, 'image_path'])

        if status == "good":
            indices_to_keep.append(idx)
            stats["good"] += 1
        else:
            stats[status] += 1
            
            if status in ["bad", "error"] and img_path.exists():
                # Vytvoríme informatívny názov súboru pre bakalárku
                safe_reason = reason.replace(" ", "_").replace(">", "gt").replace("/", "")
                new_name = f"{safe_reason}__{img_path.name}"
                dest_path = BACKUP_DIR / new_name
                
                try:
                    shutil.move(str(img_path), str(dest_path))
                except Exception as e:
                    print(f"Chyba pri presune {img_path}: {e}")

    # Vytvorenie čistého DataFrame
    df_clean = df.loc[indices_to_keep].copy()
    df_clean.to_csv(OUTPUT_CSV, sep=';', index=False, encoding='cp1250')
    real_files_count = 0

    for path in df_clean['image_path']:
        if os.path.exists(path):
            real_files_count += 1

if __name__ == "__main__":
    main()