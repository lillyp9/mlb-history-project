#testing with a small script, ran into issue where terminal show the whole raw HTML instead of getting the data I asked for 
import pandas as pd

url = "https://www.baseball-almanac.com/yearly/yr1990a.shtml"
tables = pd.read_html(url)
print(f"Total tables: {len(tables)}")
for i, table in enumerate(tables):
    print(f"\n--- Table {i} ---")
    print(table.head(3))