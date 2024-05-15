# dash.py

import plotly.graph_objs as go
import plotly.io as pio

def create_radar_chart():
    # Data for the radar chart
    ratings = {
        'worklife_balance_rating': 4,
        'salary_rating': 3,
        'work_stability_rating': 4,
        'management_rating': 3,
        'work_culture_rating': 5
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

    return chart_html
