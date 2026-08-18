import requests
import pandas as pd

def fetch_currency_data(league_name="Allflame"):
    url = f"https://poe.ninja/poe1/api/economy/exchange/current/overview?league={league_name}&type=Currency"
    
    print(f"Fetching data from: {url}")
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        print("\n--- Raw Data Successfully Extracted ---")
        
        return data
    else:
        print(f"Failed to fetch data. Error code: {response.status_code}")
        return None