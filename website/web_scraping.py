# Automated selenium test for onboarding
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
import time
from . import models

def scrape(id):
    # Retrieve the user ID passed as an argument
    user_id = id
    # Retrieve the user from the database using the user ID
    user = models.User.query.get(user_id)

    # Check if the user exists and access the company name attribute
    if user:
        company_name = user.company_name
    else:
        print("User not found or not logged in")


    # Path to the Microsoft Edge WebDriver executable
    edge_driver_path = 'testing\msedgedriver.exe'

    # Set up the Edge WebDriver service
    edge_service = Service(edge_driver_path)

    # Initialize the WebDriver object with the service
    driver = webdriver.Edge(service=edge_service)

    # Navigates to the page
    driver.get(f'https://es.indeed.com/jobs?q={company_name}&l=Madrid+provincia')    

    # Wait for the page to load
    time.sleep(3)
    '''AVERAGE POSITION COVERAGE TIME'''
    # Find all elements with the specified data-testid attribute
    date_elements = driver.find_elements(By.XPATH, "//span[@data-testid='myJobsStateDate']")
    days_list = []
    # Extract and print the text content of each date element
    for date_element in date_elements:
        # Get the text content of the element
        date_text = date_element.text
        # Remove the word "Posted" and leading/trailing whitespace
        date_text = date_text.replace("Posted", "").strip()
        date_text = date_text.replace("Publicado hace", "").strip()
        # Remove the word "Publicado" and leading/trailing whitespace
    date_text = date_text.replace("Publicado", "").strip()
    
    # Extract the number of days
    if "más de 30 días" in date_text:
        days = 31  # Assuming "más de 30 días" as 31 days for simplicity
    else:
        days = int(date_text.replace("hace", "").replace("días", "").strip())
    
    # Add the number of days to the list
    days_list.append(days)

    # Calculate the average time
    position_time = sum(days_list) / len(days_list)
    print(position_time)

    '''NUMBER OF OPEN POSITIONS'''
    li_elements = driver.find_elements(By.XPATH, "//li[contains(@class, 'css-5lfssm eu4oa1w0')]")
    number_of_positions = len(li_elements)
    print(f"Number of open positions: {number_of_positions}")


    '''BRAND SENTIMENT'''
    driver.close()