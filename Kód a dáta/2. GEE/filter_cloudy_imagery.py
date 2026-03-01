import os
import shutil
import pandas as pd
import numpy as np
from PIL import Image
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

INPUT_CSV       = Path("gee_data/results_complete.csv")
OUTPUT_CSV      = Path("gee_data/results_filtered.csv")
IMAGES_DIR      = Path("gee_data/images")
BACKUP_DIR      = Path("gee_data/removed_images")

WHITENESS_PX_TH = 240     
WHITENESS_PCT   = 20.0    
BRIGHTNESS_TH   = 200.0   
MAX_WORKERS     = 8       

BACKUP_DIR.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(INPUT_CSV, sep=None, engine="python", encoding="cp1250")
candidates = [c for c in df.columns if "path" in c.lower()]

orig_path_col = candidates[0]
df = df.rename(columns={orig_path_col: "image_path"})


def analyze(image_path_str):
    img_path = Path(image_path_str)
    if not img_path.exists():
        return image_path_str, None, None, "missing"
    try:
        img = Image.open(img_path).convert("RGB")
        arr = np.array(img)
        white_px  = np.sum(np.all(arr > WHITENESS_PX_TH, axis=2))
        total_px  = arr.shape[0] * arr.shape[1]
        white_pct = (white_px / total_px) * 100.0
        brightness = arr.mean()
        if white_pct >= WHITENESS_PCT:
            status = "cloudy"
        elif brightness >= BRIGHTNESS_TH:
            status = "bright"
        else:
            status = "good"
        return image_path_str, white_pct, brightness, status
    except Exception as e:
        return image_path_str, None, None, f"error:{e}"

paths = df["image_path"].dropna().tolist()
with ThreadPoolExecutor(MAX_WORKERS) as executor:
    results = list(executor.map(analyze, paths))

quality_map = {p: status for p, _, _, status in results}
df["status"] = df["image_path"].map(quality_map).fillna("missing")

df_good = df[df["status"] == "good"].copy()
df_good = df_good.drop_duplicates(subset="image_path", keep="first")

to_remove = [p for p, _, _, st in results if st in ("cloudy", "bright", "missing") or st.startswith("error")]
for rel_path in to_remove:
    img = Path(rel_path)
    if img.exists():
        shutil.copy(img, BACKUP_DIR / img.name)
        img.unlink()

remaining = {str((IMAGES_DIR / f).resolve())
             for f in os.listdir(IMAGES_DIR) if f.startswith("img_")}
dataset  = {str(Path(p).resolve()) for p in df_good["image_path"]}

df_good = df_good[df_good["image_path"].apply(lambda p: str(Path(p).resolve()) in remaining)]

df_good = df_good.drop(columns=["status"])
df_good.to_csv(OUTPUT_CSV, sep=";", index=False, encoding="cp1250")
