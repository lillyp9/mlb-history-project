import time
import pandas as pd
from io import StringIO #pass HTML from Selenium into pandas with StringIO wrapper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
#Where Chromerdriver lives on the system.
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"
BASE_URL = "https://www.baseball-almanac.com/yearly/yr{}a.shtml"
YEARS = range(1990, 2024) #range of years to scrape, adjust as needed

def create_driver():
    #setting help Chrome run smoother, disabling the sandboxing features that can cause issues in headless mode.
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    #launches the Chrome browser with the specified options and navigates to the given URL.
    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH),
        options=options
    ) 
    return driver

def scrape_year(driver, year):
    url = BASE_URL.format(year)
    print(f"Scrape:{year}")
    driver.get(url)
    time.sleep(3)  # Wait for the page to load
    
    try:
        html = driver.page_source
        tables = pd.read_html(StringIO(html))
       
        #Table 0 - Players Hitting Leaders Data
        hitting = tables[0].copy()
        hitting['Year'] = year
        
        #Table 2 - Team Standing Players Data
        standings = tables[2].copy()
        standings['Year'] = year
        
        return hitting, standings
    #handle erros 
    except Exception as e:
        print(f"Error scraping {year}: {e}")
        return None, None
    
def main():
    driver = create_driver()
    all_hitting = []
    all_standings = []
    
    try:
        for year in YEARS:
            hitting, standings = scrape_year(driver, year)
            if hitting is not None and standings is not None:
                all_hitting.append(hitting)
                all_standings.append(standings)
    finally:
        driver.quit()
        print("Driver closed.")
    
    # Combine all years into single DataFrames
    hitting_df = pd.concat(all_hitting, ignore_index=True)
    standings_df = pd.concat(all_standings, ignore_index=True)
    
    # Save to CSV
    hitting_df.to_csv("../data/raw/hitting_leaders.csv", index=False)
    standings_df.to_csv("../data/raw/team_standings.csv", index=False)
    print("Data saved to CSV files.") 

if __name__ == "__main__":
    main()       
        