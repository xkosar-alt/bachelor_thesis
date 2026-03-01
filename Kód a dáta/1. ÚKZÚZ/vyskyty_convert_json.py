import pandas as pd


df = pd.read_csv('vyskyty_skodcov2023-2024.csv', sep=';', encoding='windows-1250')

selected_columns = ['Datum', 'Latitude', 'Longitude', 'Škodl. org.', 'Třída výskytu']
df_satellite = df[selected_columns].copy()
df_satellite.columns = ['date', 'lat', 'lon', 'pest', 'intensity']

df_satellite['date'] = pd.to_datetime(df_satellite['date'], format='%d.%m.%Y').dt.strftime('%Y-%m-%d')

df_satellite['lat'] = df_satellite['lat'].astype(str).str.replace(',', '.', regex=False)
df_satellite['lon'] = df_satellite['lon'].astype(str).str.replace(',', '.', regex=False)

df_satellite['id'] = range(1, len(df_satellite) + 1)

df_satellite.to_json('satellite_locations.json', orient='records', indent=2, force_ascii=False)

