# Automated selenium test for signing up a user
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
import time
from faker import Faker

# Creat object to generate synthetic data 
fake = Faker()

# Path to the Microsoft Edge WebDriver executable
edge_driver_path = 'testing\msedgedriver.exe'

# Sest up the Edge WebDriver service
edge_service = Service(edge_driver_path)

# Starts the WebDriver with Edge and EdgeService
driver = webdriver.Edge(service=edge_service)

# Navigates to the page
driver.get("https://localhost:8443")

# Waits for the "Advanced" button to be clickable
avanzado_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "details-button"))
)

# Clicks the "Advanced" button
avanzado_button.click()

time.sleep(0.5)

# Waits for the "Continue to localhost" link to be clickable
continue_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Continuar a localhost"))
)

# Click the "Continue to localhost" link
continue_link.click()

'''Signs up user'''

time.sleep(1)

# Waits for the signup link to be clickable
signup_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "signUp"))
)

# Clicks the signup link
signup_link.click()

time.sleep(1)

email = fake.email()
first_name = fake.first_name()
password1= "Contraseña123&"
password2 = "Contraseña123&"
company = fake.company()
job= fake.job()
department = fake.word()

# Fills in sigunup form with synthetic data
driver.find_element(By.ID, "email").send_keys(email)
driver.find_element(By.ID, "firstName").send_keys(first_name)
driver.find_element(By.ID, "password1").send_keys(password1)
driver.find_element(By.ID, "password2").send_keys(password2)
driver.find_element(By.ID, "companyName").send_keys(company)
driver.find_element(By.ID, "jobTitle").send_keys(job)
driver.find_element(By.ID, "department").send_keys(department)

time.sleep(1)

# Clicks submit button
driver.find_element(By.XPATH, "//button[text()='Submit']").click()

time.sleep(1)

'''Logs out user'''

# Waits for the signup link to be clickable
logout_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "logout"))
)

# Clicks the logout link
logout_link.click()

time.sleep(0.5)

'''Logs in user'''

# Fills in login form with synthetic user details
driver.find_element(By.ID, "email").send_keys(email)
driver.find_element(By.ID, "password").send_keys(password1)

# Clicks submit button
driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

time.sleep(1)

driver.close()