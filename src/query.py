import sqlite3
from pathlib import Path
# find project root and define the path to the SQLite database file
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "db" / "mlb_history.db"

def query_hitting_leaders(year, team):
   #connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # Enable dictionary-like access to rows
    try:
        query = """
        SELECT
            team_standings.year,
            team_standings.team,
            team_standings.wins,
            team_standings.losses,
            hitting_leaders.player_name,
            hitting_leaders.value,
            hitting_leaders.statistic
        FROM team_standings
        JOIN hitting_leaders
            ON team_standings.year = hitting_leaders.year
            AND team_standings.team LIKE '%' || hitting_leaders.team || '%'
        WHERE team_standings.year = ?
        AND team_standings.team LIKE ?
        
        ORDER BY team_standings.wins DESC
        """
        #fetch the rows for the specified year, team, and league
        rows = conn.execute(query, (year, f'%{team}%')).fetchall()
        return rows
    finally:
        conn.close()
        
    #additional query function to get all hitting leaders for a specific year, regardless of team
    #get all teams and their hitting leaders for a given year  
def query_by_year(year):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        try:
            query = """
            SELECT
                team_standings.year,
                team_standings.team,
                team_standings.wins,
                team_standings.losses,
                hitting_leaders.player_name,
                hitting_leaders.value,
                hitting_leaders.statistic
            FROM team_standings
            JOIN hitting_leaders
                ON team_standings.year = hitting_leaders.year
                AND team_standings.team LIKE '%' || hitting_leaders.team || '%'
            WHERE team_standings.year = ?
            ORDER BY team_standings.wins DESC
            """
            rows = conn.execute(query, (year,)).fetchall()
            return rows
        finally:
            conn.close()    
    
#test out 
if __name__ == "__main__":
    print("=== Toronto Blue Jays 1990 ===")
    results = query_hitting_leaders(1990, "Toronto Blue Jays")
    print(f"Results found: {len(results)}")
    for row in results:
        print(dict(row))
    
    print("\n=== All Teams 1990 ===")
    results = query_by_year(1990)
    print(f"Results found: {len(results)}")
    for row in results:
        print(dict(row))