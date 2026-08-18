import pandas as pd

from extractor import fetch_currency_data

def clean_currency_data(raw_data):
    df_lines = pd.DataFrame(raw_data['lines'])
    df_core = pd.DataFrame(raw_data['items'])
    
    df = pd.merge(df_lines, df_core, on='id')
    
    df.drop(labels=['maxVolumeCurrency', 'maxVolumeRate', 'sparkline', 'detailsId'], axis = 1, inplace=True)
    print(df.head())
    
extracted_data = fetch_currency_data()
clean_currency_data(extracted_data)