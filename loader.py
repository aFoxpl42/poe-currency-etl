import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

def load_data_to_db(df):
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        print("Error: DATABASE_URL not found. Check your .env file.")
        return
        
    print("Connecting to Supabase...")
    engine = create_engine(db_url)
    
    table_name = "currency_history"
    
    try:
        print(f"Writing data to table: {table_name}...")
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print("Success: Data loaded to the cloud!")
    except Exception as e:
        print(f"Failed to load data: {e}")