"""
This module performs the benchmarking.
"""
from flask_login import current_user
from . import models
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import plotly.graph_objs as go
import plotly.io as pio
import time

def create_radar_chart(worklife_balance_rating, salary_rating, work_stability_rating, management_rating, work_culture_rating):
    ratings = {
        'Work Stability': work_stability_rating,
        'Salary': salary_rating,
        'Worklife Balance': worklife_balance_rating,
        'Work Culture': work_culture_rating,
        'Management': management_rating
    }

    categories = list(ratings.keys())
    values = list(ratings.values())

    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Ratings',
        marker=dict(color='#F07837'),
        line=dict(color='#F07837', width=1.3),
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 5])
        ),
        title=dict(
            text='Employee Ratings Radar Chart',
            font=dict(family="'Poppins', sans-serif", size=20),
            x=0.5,
            y=0.9,
            xanchor='center',
            yanchor='top',
        ),
        showlegend=False,
        width=600,
        height=400
    )

    return pio.to_html(fig, full_html=False)

def benchmarking():
    competitors = []

    if current_user.is_authenticated:
        user_id = current_user.id
        user_answers = models.Answers.query.filter_by(kallosusers_id=user_id).first()

        if user_answers:
            benchmark_companies = user_answers.benchmark_companies
            competitors = [company.strip() for company in benchmark_companies.split(',')]

    edge_driver_path = 'testing/msedgedriver.exe'
    edge_service = Service(edge_driver_path)
    driver = webdriver.Edge(service=edge_service)

    charts = []

    for competitor in competitors:
        driver.get(f'https://es.indeed.com/cmp/{competitor}')
        time.sleep(2)  

        ratings_dict = {}

        div_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'css-1gkra49 eu4oa1w0')]")
        for div_element in div_elements:
            rating_span = div_element.find_element(By.XPATH, ".//span[contains(@class, 'css-1qdoj65 e1wnkr790')]")
            topic_span = div_element.find_element(By.XPATH, ".//span[contains(@class, 'css-1lp75au e1wnkr790')]")

            rating_text = rating_span.text
            topic_text = topic_span.text

            ratings_dict[topic_text] = float(rating_text.replace(',', '.'))

        worklife_balance_rating = ratings_dict.get("Conciliación", 0)
        salary_rating = ratings_dict.get("Compensación y beneficios", 0)
        work_stability_rating = ratings_dict.get("Estabilidad laboral/Desarrollo profesional", 0)
        management_rating = ratings_dict.get("Gestión", 0)
        work_culture_rating = ratings_dict.get("Cultura", 0)

        chart_html = create_radar_chart(worklife_balance_rating, salary_rating, work_stability_rating, management_rating, work_culture_rating)
        charts.append((competitor, chart_html))

    driver.quit()

    return charts
