import pandas as pd
import requests
import subprocess
from io import StringIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

################################################ SCRAPING

# Chrome configuration to run in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")  # Reduces logging level
chrome_options.add_argument("--disable-logging")  # Disables logging
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Also disables logging

# Initialize the webdriver with configured options
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the page
    driver.get('https://XXXXXXXXXXXXXXXXXXXXXXX')
    
    print("Page opened")

    # Wait for the content to load
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#history-list"))
    )
        
    print("Element found")
    
    # Access the content
    content = element.text
    # print(content)
    
finally:
    # Close the browser
    driver.quit()


################################################ RAW DATA PROCESSING

# Split the content into lines
lines = content.strip().split('\n')

# Group the lines by 7 (since there are 7 columns)
grouped_lines = [lines[n:n+7] for n in range(0, len(lines), 7)]

# Create a DataFrame from the groups of lines
rawdf = pd.DataFrame(grouped_lines, columns=["Address", "Volume", "Last Trade", "Liq Margin", "Gross PnL", "Fees", "Net PnL"])

# Display the DataFrame
print(rawdf)

# Create a new DataFrame
df = rawdf

# Remove commas and dollar signs
df["Volume"] = df["Volume"].str.replace(",", "").str.replace("$", "").astype(float)
df["Liq Margin"] = df["Liq Margin"].str.replace(",", "").str.replace("$", "").astype(float)
df["Gross PnL"] = df["Gross PnL"].str.replace(",", "").str.replace("$", "").astype(float)
df["Fees"] = df["Fees"].str.replace(",", "").str.replace("$", "").astype(float)
df["Net PnL"] = df["Net PnL"].str.replace(",", "").str.replace("$", "").astype(float)

# Display the DataFrame
pd.options.display.float_format = '{:.2f}'.format
print(df)
print()

################################################ EXPORT THE DATAFRAME

# Export the DataFrame to a CSV file
df.to_csv('Traders.csv', index=False)
print("DataPosition.csv saved")
print()
