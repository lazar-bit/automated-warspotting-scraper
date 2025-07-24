import requests
import datetime
import time
import csv
import os
import pandas as pd
from typing import List, Dict

# === CONFIGURATION ===
BELLIGERENT = "russia"
BASE_URL = "https://ukr.warspotting.net/api"
HEADERS = {"User-Agent": "WarSpotClient/1.0 (contact@example.com)"}
SLEEP_BETWEEN_DATES = 2
CSV_FILE = "warspotting_losses.csv"

# === MODE DECISION ===
TODAY = datetime.date.today()
IS_SUNDAY = TODAY.weekday() == 6
IS_FULL_SCAN = IS_SUNDAY

# === DATE RANGE ===
if IS_FULL_SCAN:
    START_DATE = datetime.date(2022, 2, 24)
    END_DATE = TODAY
else:
    START_DATE = TODAY - datetime.timedelta(days=30)
    END_DATE = TODAY

# === FETCHING FUNCTION ===
def fetch_day_all_pages(date_str: str, belligerent: str) -> List[Dict]:
    all_losses = []
    page = 1
    while True:
        url = f"{BASE_URL}/losses/{belligerent}/{date_str}/{page}/" if page > 1 else f"{BASE_URL}/losses/{belligerent}/{date_str}/"
        print(f"    → Fetching: {url}")
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code == 404:
                print(f"    No data for {date_str} page {page} (404).")
                break
            r.raise_for_status()
            losses = r.json().get("losses", [])
            if not losses:
                break
            all_losses.extend(losses)
            if len(losses) < 100:
                break  # Last page
            page += 1
        except requests.RequestException as e:
            print(f"    Request error: {e}")
            break
    return all_losses

# === FLATTEN FUNCTION ===
def flatten(e: Dict) -> Dict:
    lat, lon = (None, None)
    if e.get("geo") and "," in e["geo"]:
        parts = e["geo"].split(",")
        if len(parts) == 2:
            lat, lon = parts[0].strip(), parts[1].strip()

    return {
        "id": e.get("id"),
        "date": e.get("date"),
        "type": e.get("type"),
        "model": e.get("model"),
        "status": e.get("status"),
        "lost_by": e.get("lost_by"),
        "nearest_location": e.get("nearest_location"),
        "geo": e.get("geo"),
        "latitude": lat,
        "longitude": lon,
        "unit": e.get("unit"),
        "tags": e.get("tags"),
        "comment": e.get("comment"),
        "sources": ", ".join(e.get("sources", [])) if isinstance(e.get("sources"), list) else e.get("sources"),
        "photos": ", ".join(e.get("photos", [])) if isinstance(e.get("photos"), list) else e.get("photos"),
    }

# === MAIN ===
def main():
    print(f"\n{'='*40}\nRunning {'FULL' if IS_FULL_SCAN else '30-DAY'} SCAN: {START_DATE} to {END_DATE}\n{'='*40}")
    all_data = []
    current = START_DATE

    while current <= END_DATE:
        ds = current.isoformat()
        print(f"📅 Fetching records for {ds} …")
        day_records = fetch_day_all_pages(ds, BELLIGERENT)
        flattened = [flatten(r) for r in day_records]
        all_data.extend(flattened)
        print(f"    ✓ {len(flattened)} records found for {ds}")
        current += datetime.timedelta(days=1)
        time.sleep(SLEEP_BETWEEN_DATES)

    if not all_data:
        print("\n⚠️  No data found.")
        return

    df_new = pd.DataFrame(all_data)

    if IS_FULL_SCAN or not os.path.exists(CSV_FILE):
        df_new.to_csv(CSV_FILE, index=False)
        print(f"\n✅ Wrote {len(df_new)} records to {CSV_FILE}")
    else:
        df_existing = pd.read_csv(CSV_FILE)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.drop_duplicates(subset="id", inplace=True)
        df_combined.to_csv(CSV_FILE, index=False)
        print(f"\n✅ Appended {len(df_new)} new, total {len(df_combined)} unique records to {CSV_FILE}")

if __name__ == "__main__":
    main()
