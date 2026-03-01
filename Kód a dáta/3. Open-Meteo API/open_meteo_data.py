import pandas as pd
import requests
from time import sleep

INPUT_CSV     = "gee_data/results_filtered_by_cloud_percentage.csv"
OUTPUT_CSV    = "gee_data/results_enriched.csv"
BASE_URL      = "https://archive-api.open-meteo.com/v1/archive"

HOURLY_PARAMS = [
    "temperature_2m",        
    "precipitation",          
    "windspeed_10m",        
    "cloudcover",            
    "pressure_msl",           
    "relativehumidity_2m",    
    "dewpoint_2m",            
]

TIMEZONE   = "auto"
PAUSE_SEC  = 1.0 

df = pd.read_csv(INPUT_CSV, sep=";", encoding="cp1250", parse_dates=["date"], dayfirst=True)

unique_recs = df[["date", "lat", "lon"]].drop_duplicates().reset_index(drop=True)
records     = []

# Zber hodinových dát z Open-Meteo API
for _, row in unique_recs.iterrows():
    date_str = row["date"].strftime("%Y-%m-%d")
    lat, lon = row["lat"], row["lon"]
    params = {
        "latitude":   lat,
        "longitude":  lon,
        "start_date": date_str,
        "end_date":   date_str,
        "hourly":     ",".join(HOURLY_PARAMS),
        "timezone":   TIMEZONE
    }
    resp = requests.get(BASE_URL, params=params)
    if resp.status_code != 200:
        print(f"[WARN] HTTP {resp.status_code} pre {lat},{lon} @ {date_str}")
        sleep(PAUSE_SEC)
        continue

    hourly = resp.json().get("hourly", {})
    if not hourly:
        sleep(PAUSE_SEC)
        continue

    df_h = pd.DataFrame(hourly)
    rec = {
        "date":            row["date"],
        "lat":             lat,
        "lon":             lon,
        "temp_mean":       df_h["temperature_2m"].mean(),
        "precip_sum":      df_h["precipitation"].sum(),
        "wind_mean":       df_h["windspeed_10m"].mean(),
        "cloud_mean":      df_h["cloudcover"].mean(),
        "pressure_mean":   df_h["pressure_msl"].mean(),
        "rh_mean":         df_h["relativehumidity_2m"].mean(),
        "dewpoint_mean":   df_h["dewpoint_2m"].mean(),
    }
    records.append(rec)
    sleep(PAUSE_SEC)

# Vytvorenie weather DataFrame
weather_cols = [
    "date","lat","lon",
    "temp_mean","precip_sum","wind_mean","cloud_mean",
    "pressure_mean","rh_mean","dewpoint_mean"
]
df_weather = pd.DataFrame(records, columns=weather_cols)
df_weather["date"] = pd.to_datetime(df_weather["date"])

df_merged = df.merge(df_weather, on=["date","lat","lon"], how="left")
df_merged.to_csv(OUTPUT_CSV, sep=";", index=False, encoding="cp1250")
