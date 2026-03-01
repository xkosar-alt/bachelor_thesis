import pandas as pd
import os
from PIL import Image
from tqdm import tqdm

INPUT_FILE = 'results_with_intensity_nor_ha.csv'  
OUTPUT_FILE = 'dataset_integrity_checked.csv'       

def check_image_integrity():
    df = pd.read_csv(INPUT_FILE, sep=';', encoding='cp1250')

    valid_indices = []
    missing_count = 0
    corrupt_count = 0
    
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        img_path = row['image_path']

        if not os.path.exists(img_path):
            missing_count += 1
            continue

        try:
            with Image.open(img_path) as img:
                img.verify()

            valid_indices.append(index)
            
        except (IOError, SyntaxError) as e:
            corrupt_count += 1
            print(f"Poškoedný: {img_path} ({e})")
            continue

    df_clean = df.loc[valid_indices].copy()
    df_clean.to_csv(OUTPUT_FILE, sep=';', index=False, encoding='cp1250')

if __name__ == "__main__":
    check_image_integrity()