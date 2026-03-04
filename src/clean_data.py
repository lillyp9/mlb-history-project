from pathlib import Path
import pandas as pd

#fin the project root (folder above src) and define paths for raw and clean data folders, as well as specific file paths for hitting leaders and team standings data.
PROJECT_ROOT = Path(__file__).resolve().parents[1] #go to the file , move up 1 folder and thats the project root.
#folders path 
RAW_DATA = PROJECT_ROOT / "data"/"raw"
CLEAN_DATA = PROJECT_ROOT / "data"/"clean"

#raw files 
HITTING_FILE = RAW_DATA / "hitting_leaders.csv"
STANDINGS_FILE = RAW_DATA / "team_standings.csv"

#Clean files 
HITTING_CLEAN_FILE = CLEAN_DATA / "hitting_leaders_clean.csv"
STANDINGS_CLEAN_FILE = CLEAN_DATA / "team_standings_clean.csv"

#========Cleaning Hitting Functions============
#row 1 the real columns names: statistic, player_name, team, league, value, top_25, year
def clean_hitting_data(df):
    df.columns = ['statistic', 'player_name', 'team', 'value', 'top_25', 'year']
    #drop the first two rows that are junk[title row and header row]
    df = df[df['statistic'] != 'Statistic']
    df = df[~df['statistic'].str.contains('Player Review', na=False)] #remove title row
    #remove empty rows and duplicate 
    df = df.dropna(how="all")
    df = df.drop_duplicates()
    #strip white spaces from string/text columns
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()
    #convert year to integer
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    #convert value to numeric, coerce errors to NaN (for non-numeric values
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    return df
    

#============ Clean Standing Data ==============
def clean_standings_data(df):
    df.columns = ['division', 'team', 'wins', 'losses', 'wp', 'gb', 'payroll', 'year', 'extra']
    #Drop junk rows 
    junk_patterns = [
        'Team [Click for roster]',
        'Team | Roster',
        'Click for roster',
        'American League Standings',
        'All-Star Game',
        'Standings'
    ]
    for pattern in junk_patterns:
        df = df[~df['team'].str.contains(pattern, na=False)]
        
    #keep only row where wins is actual number
    df['wins'] = pd.to_numeric(df['wins'], errors='coerce')
    df = df[df['wins'].notna()] #drop rows where wins isnt a number
    
    #remove empty rows and duplicates
    df = df.dropna(how="all")
    df = df.drop_duplicates()
    #strip white spaces from string/text columns
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()
    #convert numeric columns to appropriate data types
    for col in['losses', 'year']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    #clean payroll column by removing $ and commas, then convert to numeric
    df['payroll'] = df['payroll'].str.replace('$', '', regex=False).str.replace(',', '', regex=False)
    df['payroll'] = pd.to_numeric(df['payroll'], errors='coerce')
    return df
#============ Main Function ==============
def main():
    #load raw data 
    hitting_df = pd.read_csv(HITTING_FILE)
    standings_df = pd.read_csv(STANDINGS_FILE)
    
    #clean data 
    hitting_clean_df = clean_hitting_data(hitting_df)
    standings_clean_df = clean_standings_data(standings_df)
    
    #save cleaned data to new CSV files
    hitting_clean_df.to_csv(HITTING_CLEAN_FILE, index=False)
    standings_clean_df.to_csv(STANDINGS_CLEAN_FILE, index=False)
    print("Data cleaning complete. Cleaned files saved to:", CLEAN_DATA)
    
if __name__ == "__main__":
    main()
    