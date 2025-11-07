from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time

def scrape_fide_rankings(driver_path=None, url="https://ratings.fide.com/rankings.phtml?country=IND&gender=F"):
    """
    Scrape FIDE rankings for Indian male players with retry and long wait
    
    Args:
        driver_path: Path to chromedriver.exe (optional)
        url: URL of the FIDE rankings page
    
    Returns:
        DataFrame with player data or None if failed
    """
    
    # Set up Chrome options
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Uncomment to run in background
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Initialize the driver
    if driver_path:
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    else:
        driver = webdriver.Chrome(options=chrome_options)
    
    max_retries = 3
    df = None
    
    try:
        for attempt in range(1, max_retries + 1):
            print(f"\nAttempt {attempt}/{max_retries}: Loading page {url}")
            driver.get(url)
            
            print("Waiting 60 seconds for the page to fully load...")
            time.sleep(60)  # Give the site enough time to render
            
            try:
                wait = WebDriverWait(driver, 60)
                table_div = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "top_table_div"))
                )
                table = table_div.find_element(By.TAG_NAME, "table")
                print("✅ Table found!")
                break  # Exit retry loop if successful
                
            except Exception as e:
                print(f"⚠️ Attempt {attempt} failed: {e}")
                if attempt < max_retries:
                    print("🔁 Retrying...")
                    continue
                else:
                    print("❌ All attempts failed. Could not locate the table.")
                    return None
        
        # Extract data
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header row
        
        data = {
            'Rank': [],
            'Name': [],
            'Title': [],
            'Country': [],
            'Rating': [],
            'Birth Year': []
        }
        
        print(f"Found {len(rows)} players. Extracting data...")
        
        for row in rows:
            try:
                cells = row.find_elements(By.TAG_NAME, "td")
                
                if len(cells) >= 6:
                    data['Rank'].append(cells[0].text.strip())
                    data['Name'].append(cells[1].text.strip())
                    data['Title'].append(cells[2].text.strip())
                    data['Country'].append(cells[3].text.strip())
                    data['Rating'].append(cells[4].text.strip())
                    data['Birth Year'].append(cells[5].text.strip())
                    
            except Exception as e:
                print(f"Error processing row: {e}")
                continue
        
        df = pd.DataFrame(data)
        print(f"\n✅ Successfully extracted {len(df)} players")
        return df
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
        
    finally:
        driver.quit()


def save_to_excel(df, filename="fide_rankings_india_WOMEN.xlsx"):
    """Save DataFrame to Excel file"""
    if df is not None and not df.empty:
        df.to_excel(filename, index=False, sheet_name='Rankings')
        print(f"\n📊 Data saved to {filename}")
        print(f"Total rows: {len(df)}")
        print("\nFirst 5 rows:")
        print(df.head())
    else:
        print("No data to save.")


# Main execution
if __name__ == "__main__":
    driver_path = r'D:\chromedriver-win64\chromedriver.exe'
    
    df = scrape_fide_rankings(driver_path=driver_path)
    
    if df is not None:
        save_to_excel(df)
        df.to_csv("fide_rankings_india_WOMEN.csv", index=False)
        print("\n💾 Data also saved to fide_rankings_india.csv")
