# Automated selenium test for onboarding
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
import time
from . import models, init
from datetime import datetime


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
    driver.get(f'https://es.indeed.com/cmp/{company_name}')    

    # Wait for the page to load
    time.sleep(2)

    '''NUMBER OF POSITIONS'''
    div_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'css-181n3gf eu4oa1w0')]")
    positions_number = len(div_elements)
    print('positions: ' + str(positions_number))


    '''AVERAGE POSITION COVERAGE TIME'''
    # Find all paragraph elements with the specified class
    paragraph_elements = driver.find_elements(By.XPATH, ".//p[contains(@class, 'css-ng92tm e1wnkr790')]")

    # Initialize a list to store the number of days
    days_list = []

    # Iterate over each paragraph element found
    for paragraph_element in paragraph_elements:
        # Get the text inside the current paragraph element
        paragraph_text = paragraph_element.text
        
        # Extract the number of days from the paragraph text
        if "hace" in paragraph_text:
            days_text = paragraph_text.split(" ")[1]  # Extract the numeric part after "hace"
            if days_text.isdigit():
                days = int(days_text)
                days_list.append(days)

    average_days = None  # Initialize average_days before the conditional block

    if days_list:
        average_days = sum(days_list) / len(days_list)

    '''NUMBER OF RATINGS'''
    div_element = driver.find_element(By.XPATH, "//div[contains(@class, 'css-104u4ae eu4oa1w0')]")
    ratings_number = div_element.text
    ratings_number = float(ratings_number.replace('.', '').replace(',', '.'))  # Convert to float
    

    '''BRAND SENTIMENT'''
    ratings_dict = {}
    # Find all div elements with the specified class
    div_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'css-1gkra49 eu4oa1w0')]")
    for div_element in div_elements:
        # Find the span elements within each div
        rating_span = div_element.find_element(By.XPATH, ".//span[contains(@class, 'css-1qdoj65 e1wnkr790')]")
        topic_span = div_element.find_element(By.XPATH, ".//span[contains(@class, 'css-1lp75au e1wnkr790')]")
        
        # Extract text content from the span elements
        rating_text = rating_span.text
        topic_text = topic_span.text

        ratings_dict[topic_text] = float(rating_text)

    # Explicitly assign ratings to variables based on the Spanish topic names
    worklife_balance_rating = ratings_dict.get("Conciliación")
    salary_rating = ratings_dict.get("Compensación y beneficios")
    work_stability_rating = ratings_dict.get("Estabilidad laboral/Desarrollo profesional")
    management_rating = ratings_dict.get("Gestión")
    work_culture_rating = ratings_dict.get("Cultura")

    # Create a new instance of Surveys model with the analyzed data
    new_scrape = models.Scraping(
        kallosusers_id=user_id,
        positions_number=positions_number,
        average_days=average_days,
        ratings_number=ratings_number,
        worklife_balance_rating=worklife_balance_rating,
        salary_rating=salary_rating,
        work_stability_rating=work_stability_rating,
        management_rating=management_rating,
        work_culture_rating=work_culture_rating,
        timestamp=datetime.now()
    )

    # Add the new_surveys to the database session
    init.db.session.add(new_scrape)
    # Commit changes to the database
    init.db.session.commit()

    