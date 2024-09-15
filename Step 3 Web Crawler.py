from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time

# Set up Edge
edge_options = Options()
edge_options.add_argument("--disable-notifications")
edge_options.add_argument("--start-maximized")
edge_options.add_argument("--disable-popup-blocking")

# Initialize the WebDriver
driver = webdriver.Edge(options=edge_options)

# Go to the US BoL Website
url = "https://www.bls.gov/emp/tables/industry-occupation-matrix-industry.htm"
driver.get(url)

# Wait times to let page load
time.sleep(5)

# Locate the table element
table = driver.find_element(By.TAG_NAME, 'table')

# Retrieve all rows within the table
rows = table.find_elements(By.TAG_NAME, 'tr')

start_processing = False  # Flag to start processing from the specific row - this happens if you get a popup and you need to restart the process

for row in rows:
    cols = row.find_elements(By.TAG_NAME, 'td')
    print(f"Row has {len(cols)} columns: {[col.text for col in cols]}")  # Debugging output

    if len(cols) == 4:  # Ensure the row has exactly 4 columns
        if cols[0].text.strip() == '517000' and cols[1].text.strip() == 'Line item': # here is the start if you want to skip rows
            start_processing = True  

        if start_processing:
            try:
                industry_type = cols[1].text.strip()  # 'Line item' is in the second column
                if industry_type == "Line item":
                    matrix_link = cols[3].find_element(By.TAG_NAME, 'a').get_attribute('href')  # Link is in the fourth column
                    driver.get(matrix_link)
                    
                    time.sleep(2.5)  # Wait times to let page load
                    
                    download_button = driver.find_element(By.XPATH, '//button[text()="Download CSV"]')
                    download_button.click()
                    
                    time.sleep(5)  # Wait times to let page load
                    
                    driver.back()
            except Exception as e:
                print(f"Error processing row: {e}")
    else:
        print("Skipping row with insufficient columns")

# Close the browser
driver.quit()


# This downloads them into the "Download" folder, all files then need to be put into a "National Employment Matrix" folder in "Data"