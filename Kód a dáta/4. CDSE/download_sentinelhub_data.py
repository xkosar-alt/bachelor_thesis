import os, sys, requests, pandas as pd
from datetime import timedelta
from pyproj import Transformer
import imageio.v2 as imageio

from sentinelhub import (
    SHConfig, BBox, CRS, SentinelHubRequest, DataCollection,
    MimeType, MosaickingOrder, bbox_to_dimensions
)

for var in ["SH_PROFILE", "SH_BASE_URL", "SH_AUTH_BASE_URL", "SH_TOKEN_URL", "INSTANCE_ID"]:
    if var in os.environ:
        del os.environ[var]

# CDSE konfigurácia
CLIENT_ID = ""
CLIENT_SECRET = ""

cfg = SHConfig()
cfg.sh_client_id = CLIENT_ID
cfg.sh_client_secret = CLIENT_SECRET
cfg.sh_base_url = "https://sh.dataspace.copernicus.eu"
cfg.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
cfg.save("cdse")
config = SHConfig("cdse")

tok = requests.post(
    config.sh_token_url,
    data={"grant_type": "client_credentials",
          "client_id": config.sh_client_id,
          "client_secret": config.sh_client_secret},
    timeout=30
)
tok.raise_for_status()

CSV_PATH_IN  = "results_enriched_cleaned.csv"
CSV_PATH_OUT = "results_sentinelhub_imagery_png.csv"
OUTPUT_DIR   = "sentinel_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PATCH_SIZE_M        = 1280  
RES_M               = 10
DATE_TOLERANCE_DAYS = 0

# Evalscript pre formát png
evalscript_png = """
//VERSION=3
const minV=0.01, maxV=0.35, gamma=1.0;
function clip(x, a, b) { return x < a ? a : (x > b ? b : x); }
function enhance(v){ return Math.pow((clip(v, minV, maxV) - minV) / (maxV - minV), 1/gamma); }
function setup() {
  return {
    input: [{ bands: ["B04","B03","B02"], units: "REFLECTANCE" }],
    output: { bands: 3, sampleType: "AUTO" } // 0..1
  };
}
function evaluatePixel(s) {
  let r = enhance(s.B04);
  let g = enhance(s.B03);
  let b = enhance(s.B02);
  return [r, g, b];
}
"""

def point_square_bbox(lat, lon, size_m):
    utm_zone = int((lon + 180) / 6) + 1
    utm_epsg = f"EPSG:{32600 + utm_zone if lat >= 0 else 32700 + utm_zone}"
    from_crs = "EPSG:4326"
    to_utm = Transformer.from_crs(from_crs, utm_epsg, always_xy=True)
    to_wgs = Transformer.from_crs(utm_epsg, from_crs, always_xy=True)
    x, y = to_utm.transform(lon, lat)
    half = size_m / 2.0
    minx, miny, maxx, maxy = x - half, y - half, x + half, y + half
    lon_min, lat_min = to_wgs.transform(minx, miny)
    lon_max, lat_max = to_wgs.transform(maxx, maxy)
    return BBox([lon_min, lat_min, lon_max, lat_max], crs=CRS.WGS84)

def iso_interval_from_any(date_str, tol_days=0):
    dt = pd.to_datetime(str(date_str).strip(), dayfirst=True, errors="raise").to_pydatetime()
    start = (dt.date() - timedelta(days=tol_days)).isoformat()
    end   = (dt.date() + timedelta(days=tol_days)).isoformat()
    return start, end

def try_read_csv(path):
    encodings = ["cp1250", "latin1", "ISO-8859-1", "utf-16", "utf-8"]
    seps = [";", ",", "\t"]
    last_err = None
    for enc in encodings:
        for sep in seps:
            try:
                df = pd.read_csv(path, encoding=enc, sep=sep)
                if df.shape[1] >= 3:
                    return df
            except Exception as e:
                last_err = e
    raise last_err if last_err else RuntimeError("CSV sa nepodarilo načítať")

def normalize_headers(df):
    def clean(c): return str(c).replace("\ufeff", "").replace("\xa0", " ").strip().lower()
    df = df.copy()
    df.columns = [clean(c) for c in df.columns]
    aliases = {
        "date_used": {"date_used", "date used", "použitý dátum", "pouzity datum"},
        "date": {"date", "datum", "dátum"},
        "lat": {"lat", "latitude", "šírka", "zemepisná šírka", "zemepisna sirka"},
        "lon": {"lon", "longitude", "dĺžka", "zemepisná dĺžka", "zemepisna dlzka"},
        "image_path": {"image_path", "image pat", "image_pat", "path", "cesta"}
    }
    ren = {}
    for t, opts in aliases.items():
        for c in df.columns:
            if c in opts:
                ren[c] = t
                break
    return df.rename(columns=ren)

df_raw = try_read_csv(CSV_PATH_IN)
df = normalize_headers(df_raw)

for req in ["date_used", "lat", "lon"]:
    if req not in df.columns:
        raise ValueError(f"V CSV chýba stĺpec: {req}")
if "image_path" not in df.columns:
    df["image_path"] = ""
if "image_path_raw" not in df.columns:
    df["image_path_raw"] = "" 

# Kolekcia viazaná na CDSE host
S2L2A_CDSE = DataCollection.SENTINEL2_L2A.define_from("S2L2A_CDSE", service_url=config.sh_base_url)

success = 0
fail = 0
for i, row in df.iterrows():
    date_str = str(row["date_used"])
    lat = float(row["lat"])
    lon = float(row["lon"])

    try:
        time_interval = iso_interval_from_any(date_str, DATE_TOLERANCE_DAYS)
    except Exception as e:
        fail += 1
        continue

    bbox = point_square_bbox(lat, lon, PATCH_SIZE_M)
    width, height = bbox_to_dimensions(bbox, RES_M)

    req_png = SentinelHubRequest(
        evalscript=evalscript_png,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=S2L2A_CDSE,
                time_interval=time_interval,
                mosaicking_order=MosaickingOrder.LEAST_CC
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
        bbox=bbox,
        size=(width, height),
        config=config
    )

    try:
        data_png = req_png.get_data(save_data=False)
        if not data_png or data_png[0] is None:
            fail += 1
            continue

        iso_date = time_interval[0]
        png_name = f"S2L2A_RGB_{iso_date}_{lat:.6f}_{lon:.6f}_{width}x{height}.png"
        png_path = os.path.join(OUTPUT_DIR, png_name)
        imageio.imwrite(png_path, data_png[0])

        df.at[i, "image_path"] = f"{OUTPUT_DIR}/{png_name}"
        df.at[i, "image_path_raw"] = "" 
        success += 1

    except requests.HTTPError as e:
        detail = ""
        try: detail = e.response.text
        except Exception: pass
        fail += 1
    except Exception as e:
        fail += 1

df.to_csv(CSV_PATH_OUT, index=False)

