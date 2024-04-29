# Automated selenium test for onboarding
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

# Completes tutorial

done_button = driver.find_element(By.XPATH, "//a[text()='Done']")
done_button.click()


benchmark_companies=fake.word()
time_to_fill=fake.word()
demographic_breakdown=fake.word()
leadership_diversity=fake.word()
net_promoter_score=fake.random_number(digits=1)
employer_brand_familiarity=fake.word()


# Answers questions from bank
driver.find_element(By.ID, "benchmarkCompanies").send_keys(benchmark_companies)
driver.find_element(By.ID, "timeToFill").send_keys(time_to_fill)
driver.find_element(By.ID, "demographicBreakdown").send_keys(demographic_breakdown)
driver.find_element(By.ID, "leadershipDiversity").send_keys(leadership_diversity)
driver.find_element(By.ID, "NPS").send_keys(net_promoter_score)
driver.find_element(By.ID, "brandFamiliarity").send_keys(employer_brand_familiarity)


# Clicks submit button
driver.find_element(By.XPATH, "//button[text()='Submit']").click()

# Clicks submit button for surveys
upload_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Upload']")

# Click the "Upload" button
upload_button.click()

time.sleep(1)

driver.close()
