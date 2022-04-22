
import time
from datetime import datetime

# Import Selenium and appropriate modules
# Using webdriver_manager so we don't have to mess around with driver executables.

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Finding geolocation values from postcode.
import pgeocode

# Set up geolocation to convert postcode to long/lat
set_geolocation = pgeocode.Nominatim('GB')

# Change for different radius of chartiy shop 
# around given location
location = "PO4 0EJ"
location_results = []

# Uses the chrome driver to load up the website
driver = webdriver.Chrome(ChromeDriverManager().install())

# Grabs the salvation army website
driver.get('https://www.salvationarmydonationcentre.org/bank-finder')

# Finds the text box for inputting our chosen location
text_input_box = driver.find_element(by=By.TAG_NAME, value="input")
text_input_box.send_keys(location)

# Once we have input our location, this will "press" the button to show results
text_input_button = driver.find_element(by=By.CLASS_NAME, value="button")
text_input_button.click()

# Give the website a moment to load results before checking for them
time.sleep(1)

# Search for the final button, changing the results from map view (default) to list view
list_view_button = driver.find_element_by_xpath("// div[contains(text(),\'List')]")
list_view_button.click()


# Compile the results by looking for the result class
find_results = driver.find_elements(by=By.CLASS_NAME, value="result")

# Iterate through the located results, making them acceptable for entry into the database.
# Also calculates the geolocation from postcode using the pgeocode module

for result in find_results:
    result_lines = result.text.splitlines()

    get_postcode = result_lines[1].split(",")
    get_geo = set_geolocation.query_postal_code(get_postcode[-1])

    final_geo = f"{get_geo['latitude']},{get_geo['longitude']}"

    result_dict = (result_lines[0], datetime.now(), datetime.now(), result_lines[1], final_geo, 2)

    location_results.append(result_dict) 

db_connection.executemany('INSERT OR REPLACE INTO charitymap_location(name, created_at, updated, address, geolocation, type) VALUES (?,?,?,?,?,?)', location_results)
db_connection.commit()
