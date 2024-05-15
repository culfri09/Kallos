import plotly.graph_objs as go
import plotly.io as pio
from flask_login import current_user
from . import models

def create_charts():
    if current_user.is_authenticated:
        user_id = current_user.id
        user_scrapes = models.Scraping.query.filter_by(kallosusers_id=user_id).first()
        user_surveys = models.Surveys.query.filter_by(kallosusers_id=user_id).first()
        user_answers = models.Answers.query.filter_by(kallosusers_id=user_id).first()

        radar_chart_html = None
        line_graph_html = None
        ratings_number = None

        if user_scrapes:
            worklife_balance_rating = user_scrapes.worklife_balance_rating
            salary_rating = user_scrapes.salary_rating
            work_stability_rating = user_scrapes.work_stability_rating
            management_rating = user_scrapes.management_rating
            work_culture_rating = user_scrapes.work_culture_rating
            ratings_number = user_scrapes.ratings_number

            # Create radar chart for ratings
            radar_chart_html = create_radar_chart(
                worklife_balance_rating,
                salary_rating,
                work_stability_rating,
                management_rating,
                work_culture_rating
            )

        if user_surveys:
            enps = user_surveys.enps
            candidate_rate = user_surveys.candidate_rate
            retention_rate = user_surveys.retention_rate
            workplace_rate = user_surveys.workplace_rate

            # Create line graph for employee engagement
            line_graph_html = create_line_graph(
                enps,
                candidate_rate,
                retention_rate,
                workplace_rate
            )

            if user_answers:
                 
                development = user_answers.development
                if development is not None:
                    # Convert percentage string to float
                    development = float(development.strip('%'))  # Remove '%' symbol and convert to float
                    # Ensure development is within 0-100 range (assuming it's a percentage)
                    development = max(0, min(development, 100))

                    # Create donut chart for development
                    gauge_chart_html = create_gauge_chart(development)
                investment=user_answers.investment
                employer_brand_familiarity=user_answers.employer_brand_familiarity
                bar_chart_html=create_bar_chart(investment, employer_brand_familiarity)


            if user_answers and user_scrapes:
                channels = user_answers.channels.split(', ')
                positions_number = user_scrapes.positions_number
                average_days=user_scrapes.average_days
                stacked_bar_chart_html =create_stacked_bar_chart(channels, positions_number, average_days)

        return radar_chart_html, line_graph_html, gauge_chart_html, stacked_bar_chart_html,bar_chart_html, ratings_number
    
    return None, None, None, None

def create_radar_chart(worklife_balance_rating, salary_rating, work_stability_rating, management_rating, work_culture_rating):
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

    return chart_html

def create_line_graph(enps, candidate_rate, retention_rate, workplace_rate):
    # Data for the line graph
    x_values = ['ENPS', 'Candidate Rate', 'Retention Rate', 'Workplace Rate']
    y_values = [enps, candidate_rate, retention_rate, workplace_rate]

    # Creating line graph
    fig = go.Figure(data=go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines+markers',
        name='Employee Engagement'
    ))

    # Layout
    fig.update_layout(
        title='Employee Engagement Metrics',
        xaxis_title='Metrics',
        yaxis_title='Values',
        width=600,  
        height=400
    )

    # Convert the graph to HTML
    graph_html = pio.to_html(fig, full_html=False)

    return graph_html

def create_gauge_chart(development):
    # Check if development data is available and valid
    if development is None or not isinstance(development, (int, float)):
        return None
    
    # Creating Gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=development,
        title={'text': "Talent Development"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': "#63A4FF"}}))

    # Layout
    fig.update_layout(
        title='Talent Development',
        width=600,
        height=400
    )

    # Convert the chart to HTML
    chart_html = pio.to_html(fig, full_html=False)

    return chart_html

def create_stacked_bar_chart(channels,positions_number,average_days):
    # Data for the stacked bar chart
    categories = channels
    positions = [positions_number] * len(channels)  # Ensure positions is a list of the same length as channels
    days_to_fill = [average_days] * len(channels)  # Ensure days_to_fill is a list of the same length as channels

    # Creating the stacked bar chart
    fig = go.Figure(data=[
        go.Bar(name='Positions', x=categories, y=positions),
        go.Bar(name='Average Days to Fill', x=categories, y=days_to_fill)
    ])

    # Layout
    fig.update_layout(
        barmode='stack',
        title='Recruitment Metrics',
        xaxis_title='Recruitment Channels',
        yaxis_title='Metrics',
        width=800,
        height=500
    )

    # Convert the chart to HTML
    chart_html = pio.to_html(fig, full_html=False)

    return chart_html


def create_bar_chart(investment, employer_brand_familiarity):
        # Data for the bar chart
    data = [
        go.Bar(
            x=[employer_brand_familiarity],
            y=[investment],
            name='Investment in Employer Brand Initiatives'
        )
    ]

    # Layout
    layout = go.Layout(
        title='Employer Branding Metrics',
        xaxis=dict(title='Familiarity Level'),
        yaxis=dict(title='Investment (in money)')
    )

    # Create the figure
    fig = go.Figure(data=data, layout=layout)

    # Convert the chart to HTML
    chart_html = pio.to_html(fig, full_html=False)

    return chart_html