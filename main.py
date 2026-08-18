from extractor import fetch_currency_data
from transformer import clean_currency_data

raw_data = fetch_currency_data()

if raw_data is None:
    print("Pipeline aborted: Extraction failed.")
else:
    clean_df = clean_currency_data(raw_data)
