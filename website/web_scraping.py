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
    user_id = id
    user = models.User.query.get(user_id)

    if user:
        company_name = user.company_name
    else:
        print("User not found or not logged in")

    edge_driver_path = 'testing\msedgedriver.exe'

    edge_service = Service(edge_driver_path)

    driver = webdriver.Edge(service=edge_service)

    driver.get(f'https://es.indeed.com/cmp/{company_name}')    

    time.sleep(2)

    '''NUMBER OF POSITIONS'''
    div_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'css-181n3gf eu4oa1w0')]")
    positions_number = len(div_elements)
    print('positions: ' + str(positions_number))

    '''AVERAGE POSITION COVERAGE TIME'''
    paragraph_elements = driver.find_elements(By.XPATH, ".//p[contains(@class, 'css-ng92tm e1wnkr790')]")

    days_list = []

    for paragraph_element in paragraph_elements:
        paragraph_text = paragraph_element.text

        if "hace" in paragraph_text:
            days_text = paragraph_text.split(" ")[1]
            if days_text.isdigit():
                days = int(days_text)
                days_list.append(days)

    average_days = None  

    if days_list:
        average_days = sum(days_list) / len(days_list)

    '''NUMBER OF RATINGS'''
    div_element = driver.find_element(By.XPATH, "//div[contains(@class, 'css-104u4ae eu4oa1w0')]")
    ratings_number = div_element.text
    ratings_number = float(ratings_number.replace('.', '').replace(',', '.'))

    '''BRAND SENTIMENT'''
    ratings_dict = {}

    div_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'css-1gkra49 eu4oa1w0')]")
    for div_element in div_elements:
        rating_span = div_element.find_element(By.XPATH, ".//span[contains(@class, 'css-1qdoj65 e1wnkr790')]")
        topic_span = div_element.find_element(By.XPATH, ".//span[contains(@class, 'css-1lp75au e1wnkr790')]")

        rating_text = rating_span.text
        topic_text = topic_span.text

        
        ratings_dict[topic_text] = float(rating_text.replace(',', '.'))

    worklife_balance_rating = ratings_dict.get("Conciliación")
    salary_rating = ratings_dict.get("Compensación y beneficios")
    work_stability_rating = ratings_dict.get("Estabilidad laboral/Desarrollo profesional")
    management_rating = ratings_dict.get("Gestión")
    work_culture_rating = ratings_dict.get("Cultura")

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

    init.db.session.add(new_scrape)
    init.db.session.commit()


    