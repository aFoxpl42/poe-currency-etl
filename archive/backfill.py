import requests
import time
import pandas as pd

from extractor import fetch_currency_data
from loader import load_data_to_db

# One time use function to fill values of curriencies from the start of the league
def backfill(league_name = "Allflame"):
    categories = ["Fragment", "Scarab"]
    for category in categories:
        raw_data = fetch_currency_data(league_name, category)
        if raw_data is None:
            print("Couldn't backfill values: extraction failed.")
            return None
        
        df_items = pd.DataFrame(raw_data['items'])
        old_rows = [] # list of dictionaries
        fails = [] # list of failed ids
        
        for id in df_items['detailsId']:
            print(f"Fetching history for ID: {id}")
            time.sleep(1)
            
            url = f"https://poe.ninja/poe1/api/economy/exchange/current/details?league={league_name}&type={category}&id={id}"
            response = requests.get(url)
            
            if response.status_code == 200 or response.status_code == 304:
                currency_data = response.json() 
                
                if 'pairs' in currency_data and len(currency_data['pairs']) > 0:
                    for ts in currency_data['pairs'][0].get('history', []):
                        old_rows.append({
                            'id': currency_data["item"]["id"],
                            'primaryValue': ts['rate'],
                            'volumePrimaryValue': ts['volumePrimaryValue'],
                            'name': currency_data['item']['name'],
                            'image': currency_data['item'].get('image', ''),
                            'category': currency_data['item']['category'],
                            'time': pd.to_datetime(ts.get('timestamp'))
                        })
                    
            else:
                print(f"Failed to fetch data for {id}. Error code: {response.status_code}")
                print(f"Url used: {url}")
                fails.append(id)
                continue
            
            
        print(f"Finished fetching. Compiling {len(old_rows)} rows of data.\n")
        backfill_df = pd.DataFrame(old_rows)
        print(old_rows)
        print(f"Failed ids: {fails}")
        
        load_data_to_db(backfill_df)
    
backfill()