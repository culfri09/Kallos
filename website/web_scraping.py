# Automated selenium test for onboarding
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
import time
from selenium.webdriver.common.keys import Keys

# Path to the Microsoft Edge WebDriver executable
edge_driver_path = 'testing\msedgedriver.exe'

# Set up the Edge WebDriver service
edge_service = Service(edge_driver_path)

# Initialize the WebDriver object with the service
driver = webdriver.Edge(service=edge_service)

# Navigates to the page
driver.get("https://es.indeed.com/jobs?q=alcampo&l=Madrid+provincia&from=searchOnHP&vjk=617f2cc1d4734ff6")

# Wait for the page to load
time.sleep(3)

# Find all elements with the specified data-testid attribute
date_elements = driver.find_elements(By.XPATH, "//span[@data-testid='myJobsStateDate']")

# Extract and print the text content of each date element
for date_element in date_elements:
    # Get the text content of the element
    date_text = date_element.text
    # Remove the word "Posted" and leading/trailing whitespace
    date_text = date_text.replace("Posted", "").strip()
    # Print the modified text
    print(date_text)

time.sleep(100)