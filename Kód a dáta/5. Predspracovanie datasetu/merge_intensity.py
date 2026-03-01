import pandas as pd
import numpy as np

RESULTS_FILE = 'results_sentinelhub_imagery_updated.csv'
VYSKYTY_FILE = 'vyskyty_skodcov2023-2024.csv'
OUTPUT_FILE = 'results_with_intensity_nor_ha.csv'

def merge_datasets():
    df_results = pd.read_csv(RESULTS_FILE, sep=';', encoding='cp1250')
    df_vyskyty = pd.read_csv(VYSKYTY_FILE, sep=';', decimal=',', encoding='cp1250')

    df_vyskyty_subset = df_vyskyty[['Datum', 'Latitude', 'Longitude', 'Škodl. org.', 'Intenzita']].copy()
    
    df_vyskyty_subset.rename(columns={
        'Datum': 'date',
        'Latitude': 'lat',
        'Longitude': 'lon',
        'Škodl. org.': 'pest',
        'Intenzita': 'intensity_nor_ha'
    }, inplace=True)

    df_vyskyty_subset['intensity_nor_ha'] = pd.to_numeric(df_vyskyty_subset['intensity_nor_ha'], errors='coerce')

    df_results['lat'] = pd.to_numeric(df_results['lat'], errors='coerce')
    df_results['lon'] = pd.to_numeric(df_results['lon'], errors='coerce')
    df_results['lat_round'] = df_results['lat'].round(5)
    df_results['lon_round'] = df_results['lon'].round(5)
    df_vyskyty_subset['lat_round'] = df_vyskyty_subset['lat'].round(5)
    df_vyskyty_subset['lon_round'] = df_vyskyty_subset['lon'].round(5)

    df_vyskyty_subset.drop_duplicates(subset=['date', 'lat_round', 'lon_round', 'pest'], keep='first', inplace=True)

    merged_df = pd.merge(
        df_results,
        df_vyskyty_subset[['date', 'lat_round', 'lon_round', 'pest', 'intensity_nor_ha']],
        on=['date', 'lat_round', 'lon_round', 'pest'],
        how='left'
    )

    merged_df['intensity_nor_ha'] = merged_df['intensity_nor_ha'].fillna(0)
    merged_df['intensity_nor_ha'] = merged_df['intensity_nor_ha'].astype(int)

    merged_df.drop(columns=['lat_round', 'lon_round'], inplace=True)
    
    cols = list(merged_df.columns)
    if 'intensity_nor_ha' in cols:
        cols.remove('intensity_nor_ha')
        try:
            target_idx = cols.index('intensity') + 1
        except ValueError:
            target_idx = len(cols)
        cols.insert(target_idx, 'intensity_nor_ha')
        merged_df = merged_df[cols]

    merged_df.to_csv(OUTPUT_FILE, sep=';', index=False, encoding='cp1250')

if __name__ == "__main__":
    merge_datasets()