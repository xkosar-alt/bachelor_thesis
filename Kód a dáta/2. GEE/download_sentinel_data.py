import ee 
import os 
import json 
import pandas as pd 
from datetime import datetime, timedelta 
import requests 
import time 
 
# Inicializácia GEE
try: 
    ee.Initialize(project='pest-detection-czechia') 
except Exception as e: 
    ee.Authenticate() 
    ee.Initialize(project='pest-detection-czechia') 
 
os.makedirs('gee_data', exist_ok=True) 
os.makedirs('gee_data/images', exist_ok=True) 
 
with open('satellite_locations.json', 'r', encoding='utf-8') as f: 
    locations = json.load(f) 
 
 
# Funkcia ee na počítanie všetkých spektrálnych indexov 
def calculateIndices(image): 
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI') 
    ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI') 
    ndmi = image.normalizedDifference(['B8', 'B11']).rename('NDMI') 
    gndvi = image.normalizedDifference(['B8', 'B3']).rename('GNDVI') 
    reci = image.select('B5').divide(image.select('B4')).subtract(ee.Image(1)).rename('RECI') 
 
    return image.addBands([ndvi, ndwi, ndmi, gndvi, reci]) 
 
 
# Funkcia na stiahnutie snímky
def download_image(image, point, date_str, lat, lon, scale=10, buffer_size=200): 
    try: 
        buffer = ee.Geometry.Point([float(lon), float(lat)]).buffer(buffer_size) 
 
        # Získanie URL obrázka 
        url = image.visualize( 
            bands=['B4', 'B3', 'B2'], 
            min=0, 
            max=3000, 
            gamma=1.4 
        ).getThumbURL({ 
            'region': buffer, 
            'dimensions': '256x256', 
            'format': 'png' 
        }) 
 
        # Stiahnutie obrázka 
        response = requests.get(url) 
        if response.status_code == 200: 
            file_path = f"gee_data/images/img_{lat}_{lon}_{date_str}.png" 
            with open(file_path, 'wb') as f: 
                f.write(response.content) 
            return file_path 

 
    except Exception as e: 
        print(f"Problém pri sťahovaní snímky: {lat}, {lon}, {date_str}, {str(e)}") 
        return None 
 
 
# Funkcia na spracovanie jednej lokality 
def process_location(loc): 
    try: 
        loc_id = loc['id'] 
        date_str = loc['date'] 
        lat = float(loc['lat']) 
        lon = float(loc['lon']) 
 
 
        # Vytvorenie časového okna ±5 dní 
        date = datetime.strptime(date_str, '%Y-%m-%d') 
        start_date = (date - timedelta(days=5)).strftime('%Y-%m-%d') 
        end_date = (date + timedelta(days=5)).strftime('%Y-%m-%d') 
 
        point = ee.Geometry.Point([lon, lat]) 
 
        # Filtrovanie Sentinel-2 snímok 
        s2_collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') 
                         .filterBounds(point) 
                         .filterDate(start_date, end_date) 
                         .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) 
                         .sort('CLOUDY_PIXEL_PERCENTAGE')) 
 
        # Kontrola, či sú dostupné snímky 
        count = s2_collection.size().getInfo() 
        if count == 0: 
            return { 
                'id': loc_id, 
                'date': date_str, 
                'lat': lat, 
                'lon': lon, 
                'pest': loc.get('pest', ''), 
                'intensity': loc.get('intensity', ''), 
                'NDVI': None, 
                'NDWI': None, 
                'NDMI': None, 
                'GNDVI': None, 
                'RECI': None, 
                'red': None, 
                'nir': None, 
                'date_used': None, 
                'image_path': None, 
                'cloud_percentage': None 
            } 
 
        # Získanie najlepšej snímky (s najnižšou oblačnosťou) 
        best_image = s2_collection.first() 
 
        image_with_indices = calculateIndices(best_image) 
        image_date = ee.Date(best_image.get('system:time_start')).format('YYYY-MM-dd').getInfo() 
        cloud_percentage = best_image.get('CLOUDY_PIXEL_PERCENTAGE').getInfo() 
 
        point_values = image_with_indices.reduceRegion( 
            reducer=ee.Reducer.mean(), 
            geometry=point, 
            scale=10
        ).getInfo() 
 
        # Stiahnutie obrázka 
        image_path = download_image(best_image, point, date_str, lat, lon) 
 
        result = { 
            'id': loc_id, 
            'date': date_str, 
            'lat': lat, 
            'lon': lon, 
            'pest': loc.get('pest', ''), 
            'intensity': loc.get('intensity', ''), 
            'NDVI': point_values.get('NDVI'), 
            'NDWI': point_values.get('NDWI'), 
            'NDMI': point_values.get('NDMI'), 
            'GNDVI': point_values.get('GNDVI'), 
            'RECI': point_values.get('RECI'), 
            'red': point_values.get('B4'), 
            'nir': point_values.get('B8'), 
            'date_used': image_date, 
            'image_path': image_path, 
            'cloud_percentage': cloud_percentage 
        } 
 
        return result 
 
    except Exception as e: 
        print(f"Chyba pri lokalite {loc.get('id', 'N/A')}: {str(e)}") 
        return { 
            'id': loc.get('id', 'N/A'), 
            'date': loc.get('date', ''), 
            'lat': loc.get('lat', ''), 
            'lon': loc.get('lon', ''), 
            'pest': loc.get('pest', ''), 
            'intensity': loc.get('intensity', ''), 
            'error': str(e) 
        } 
 
 
def main(): 
    all_results = [] 
 
    for i, loc in enumerate(locations): 
        result = process_location(loc) 
        all_results.append(result) 
 
        time.sleep(0.5) 

    df = pd.DataFrame(all_results) 
    df.to_csv('gee_data/results_complete.csv', index=False, sep=';', encoding='utf-8-sig') 
 
    with open('gee_data/results_complete.json', 'w', encoding='utf-8') as f: 
        json.dump(all_results, f, indent=2, ensure_ascii=False) 
 
 
if __name__ == "__main__": 
    main() 
 