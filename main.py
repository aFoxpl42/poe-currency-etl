from extractor import fetch_currency_data
from transformer import clean_currency_data
from loader import load_data_to_db

def run_pipeline():
    print("--- Starting ETL Pipeline ---")
    
    raw_data = fetch_currency_data("Allflame")
    if raw_data is None:
        print("Pipeline aborted: Extraction failed.")
        return
        
    clean_df = clean_currency_data(raw_data)
    if clean_df is None or clean_df.empty:
        print("Pipeline aborted: Transformation resulted in empty data.")
        return
        
    load_data_to_db(clean_df)
    
    print("--- ETL Pipeline Completed Successfully ---")

if __name__ == "__main__":
    run_pipeline()