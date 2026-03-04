from pathlib import Path
import pandas as pd
import sqlite3

#project root and data paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEAN_DATA = PROJECT_ROOT /"data" / "clean"
DB_DATA = PROJECT_ROOT / "db"

#database file path
DB_FILE = DB_DATA / "mlb_history.db"

#clean CSV file paths
HITTING_CLEAN_FILE = CLEAN_DATA / "hitting_leaders_clean.csv"
STANDINGS_CLEAN_FILE = CLEAN_DATA / "team_standings_clean.csv"

#import the CSV files into SQLite database
def main():
    #connect to the SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect(DB_FILE)
    
    try:
        #import hitting leaders data
        hitting_df = pd.read_csv(HITTING_CLEAN_FILE)
        hitting_df.to_sql("hitting_leaders", conn, if_exists="replace", index=False)
        
        #import team standings data
        standings_df = pd.read_csv(STANDINGS_CLEAN_FILE)
        standings_df.to_sql("team_standings", conn, if_exists="replace", index=False)
        
        print("Data imported successfully into SQLite database.")
    finally:
        conn.close()
        print("Database connection closed.")
        
if __name__ == "__main__":
    main()