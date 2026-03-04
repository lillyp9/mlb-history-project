import time
import pandas as pd
from io import StringIO #pass HTML from Selenium into pandas with StringIO wrapper
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
#Where Chromerdriver lives on the system.
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

URL_1990_AL = ("https://www.baseball-almanac.com/yearly/yr1990a.shtml")

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

def perview_tables(driver):
    # Find all tables on the page
    html = driver.page_source
    tables = pd.read_html(StringIO(html))
    print(f"Total tables found: {len(tables)}")
    # Print the rows in tables after looping through them
    for i, table in enumerate(tables):
        print(f"\n--- Table INDEX: {i} ---")
        print(table.head(5))  # Print first 5 rows of each table
        
def main():
    driver = create_driver()
    try:
        print("Opening URL:", URL_1990_AL)
        driver.get(URL_1990_AL)
        time.sleep(3)  # Wait for the page to load
        
        print("Page title:", driver.title)
        perview_tables(driver)
    finally:
        driver.quit()
        print("Driver closed.")
        
if __name__ == "__main__":
    main()
    
        
