# dash.py

import plotly.graph_objs as go
import plotly.io as pio
from flask_login import current_user
from . import models

def create_radar_chart():
    if current_user.is_authenticated:
        user_id = current_user.id
        # Query existing answer record for the current user
        user_scrapes = models.Scraping.query.filter_by(kallosusers_id=user_id).first()

        if user_scrapes:
            ratings_number = user_scrapes.ratings_number
            worklife_balance_rating = user_scrapes.worklife_balance_rating
            salary_rating = user_scrapes.salary_rating
            work_stability_rating = user_scrapes.work_stability_rating
            management_rating = user_scrapes.management_rating
            work_culture_rating = user_scrapes.work_culture_rating
            # Data for the radar chart
            ratings = {
                'worklife_balance_rating': worklife_balance_rating,
                'salary_rating': salary_rating,
                'work_stability_rating': work_stability_rating,
                'management_rating': management_rating,
                'work_culture_rating': work_culture_rating
            }

            # Extracting category names and ratings
            categories = list(ratings.keys())
            values = list(ratings.values())

            # Creating radar chart
            fig = go.Figure(data=go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Ratings'
            ))

            # Layout
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5]  # Adjust the range as per your requirement
                    )
                ),
                showlegend=False,
                title='Employee Ratings Radar Chart',
                width=600,  # Adjust width as needed
                height=400  # Adjust height as needed
            )

            # Convert the chart to HTML
            chart_html = pio.to_html(fig, full_html=False)

            return chart_html,ratings_number  # Return the radar chart HTML and ratings_number
    return None, None  # Return None if current_user is not authenticated or no data found
