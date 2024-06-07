"""
This module creates the dashboard.
"""
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
        gauge_chart_html = None
        stacked_bar_chart_html = None
        bar_chart_html = None
        horizontal_bar_chart_html = None

        if user_scrapes:
            worklife_balance_rating = user_scrapes.worklife_balance_rating
            salary_rating = user_scrapes.salary_rating
            work_stability_rating = user_scrapes.work_stability_rating
            management_rating = user_scrapes.management_rating
            work_culture_rating = user_scrapes.work_culture_rating
            ratings_number = user_scrapes.ratings_number

            # Creates radar chart for ratings
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

            # Create sline graph for employee engagement
            line_graph_html = create_line_graph(
                enps,
                candidate_rate,
                retention_rate,
                workplace_rate
            )

            if user_answers:
                development = user_answers.development
                if development is not None:
                    # Converts percentage string to float
                    development = float(development.strip('%').rstrip('.').strip())  # Remove '%' symbol and convert to float
                    # Ensures development is within 0-100 range (assuming it's a percentage)
                    development = max(0, min(development, 100))

                    # Creates donut chart for development
                    gauge_chart_html = create_gauge_chart(development)

                investment = user_answers.investment
                employer_brand_familiarity = user_answers.employer_brand_familiarity
                bar_chart_html = create_bar_chart(investment, employer_brand_familiarity)

                demographic_breakdown = user_answers.demographic_breakdown
                if demographic_breakdown is not None:
                    demographic_breakdown = demographic_breakdown.split(', ')
                    leadership_diversity = user_answers.leadership_diversity
                    horizontal_bar_chart_html = create_horizontal_bar_chart(leadership_diversity, demographic_breakdown)

                channels = user_answers.channels
                if channels is not None:
                    channels = channels.split(', ')
                    positions_number = user_scrapes.positions_number
                    average_days = user_scrapes.average_days
                    stacked_bar_chart_html = create_stacked_bar_chart(channels, positions_number, average_days)

        return radar_chart_html, line_graph_html, gauge_chart_html, stacked_bar_chart_html, bar_chart_html, horizontal_bar_chart_html, ratings_number

    return None, None, None, None, None, None, None

def create_radar_chart(worklife_balance_rating, salary_rating, work_stability_rating, management_rating, work_culture_rating):
 # Data for the radar chart
    ratings = {
        'Work Stability': work_stability_rating,
        'Salary': salary_rating,
        'Worklife Balance': worklife_balance_rating,
        'Work Culture': work_culture_rating,
        'Management': management_rating
    }

    # Extracting category names and ratings
    categories = list(ratings.keys())
    values = list(ratings.values())

    # Creating radar chart
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Ratings',
        marker=dict(
            color='#F07837',  # Border and point color
        ),
        line=dict(
            color='#F07837',  # Line color
            width=1.3,  # Border width
        ),
    ))

    # Layout
    fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 5]  # Adjusts the range as per your requirement
        )
    ),
    title=dict(
        text='Employee Ratings Radar Chart',
        font=dict(
            family="'Poppins', sans-serif",  # Font family
            size=20,  # Font size
        ),
        x=0.5, 
        y=0.9,  
        xanchor='center',  
        yanchor='top',  
    ),
    showlegend=False,
    width=600, 
    height=400  
)

    # Converts the chart to HTML
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
        name='Employee Engagement',
        line=dict(
            color='#F07837'  # Line color
        ),
        marker=dict(
            color='#F07837'  # Marker color
        )
    ))

    # Layout
    fig.update_layout(
        title=dict(
            text='Employee Engagement',
            font=dict(
                family="'Poppins', sans-serif",  # Font family
                size=20,  # Font size
            ),
            x=0,  
            xanchor='left', 
            y=0.9,  
            yanchor='top',  
            pad=dict(l=170)  
        ),
        xaxis=dict(
            title='Metrics',
            showgrid=True,
            gridcolor="rgba(0,0,0,0.05)",
            autorange='reversed'  
        ),
        yaxis=dict(
            title='Values',
            showgrid=True,
            gridcolor="rgba(0,0,0,0)",
            zeroline=True,
            zerolinecolor="rgba(0,0,0,0.05)",
            zerolinewidth=2
        ),
        plot_bgcolor='rgba(0,0,0,0)',  
        paper_bgcolor='rgba(0,0,0,0)', 
        width=600,  
        height=400,
        font=dict(
            family="'Poppins', sans-serif"  
        )
    )

    # Converts the graph to HTML
    graph_html = pio.to_html(fig, full_html=False)

    return graph_html

def create_gauge_chart(development):
    # Check sif development data is available and valid
    if development is None or not isinstance(development, (int, float)):
        return None

    # Creating Gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=development,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#fad9c7"},  
            'borderwidth': 2,
            'bordercolor': "white",  
            'steps': [
                {'range': [0, 50], 'color': "rgba(99, 164, 255, 0.2)"}, 
                {'range': [50, 100], 'color': "rgba(99, 164, 255, 0.4)"}  
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': development
            }
        },
        number={
            'font': {'family': "'Poppins', sans-serif"}  
        }
    ))

    # Layout
    fig.update_layout(
        title=dict(
            text='Talent Development',
            font=dict(
                family="'Poppins', sans-serif",  
                size=20,  
            ),
            x=0.5,  
            y=0.9, 
            xanchor='center', 
            yanchor='top',
        ),
        font=dict(
            family="'Poppins', sans-serif"  
        ),
        width=600,
        height=400
    )

    # Converts the chart to HTML
    chart_html = pio.to_html(fig, full_html=False)

    return chart_html

def create_stacked_bar_chart(channels,positions_number,average_days):
    # Ensures positions_number and average_days are lists
    positions = [positions_number] * len(channels)
    
    fig = go.Figure(data=[
        go.Bar(name='Number of Positions', x=channels, y=positions, marker_color='#fad9c7', width=0.05),  
       # go.Bar(name='Average Days to Fill', x=channels, y=[average_days], marker_color='#F07837', width=0.4)  # Set Days to Fill color to orange and adjust bar width
        go.Bar(name='Average Days to Fill', x=channels, y=[], marker_color='#F07837', width=0.4)
    ])

    # Layout
    fig.update_layout(
        title=dict(
            text='Recruitment',
            font=dict(
                family="'Poppins', sans-serif", 
                size=20,  
            ),
            x=0.5,  
            y=0.9,  
            xanchor='center',  
            yanchor='top',  
        ),
        barmode='group',
        width=600,  
        height=400,  
        font=dict(
            family="'Poppins', sans-serif"  
        ),
        legend=dict(
            orientation='h',  
            yanchor='bottom',  
            y=1.02,  
            xanchor='center', 
            x=0.5  
        ),
        plot_bgcolor='white',  
        xaxis=dict(
            gridcolor='#f3f5f6',  
        ),
        yaxis=dict(
            gridcolor='#f3f5f6',  
        )
    )

    # Converts the chart to HTML
    chart_html = pio.to_html(fig, full_html=False)

    return chart_html

def create_bar_chart(investment, employer_brand_familiarity):
    data = [
        go.Bar(
            x=["Very Familiar", "Familiar", "Not Very Familiar"],
            y=[0, employer_brand_familiarity, 0],
            name='Familiarity',
            marker=dict(color='#fad9c7', line=dict(color="orange", width=1)), 
            width=0.1  
        ),
        go.Bar(
            x=["Very Familiar", "Familiar", "Not Very Familiar"],
            y=[0, investment, 0],
            name='Investment',
            marker=dict(color='#F07837', line=dict(color="darkorange", width=1)),  
            width=0.1  
        )
    ]

    # Layout
    layout = go.Layout(
        title=dict(
            text='Employer Branding',
            font=dict(
                family="'Poppins', sans-serif",  
                size=20,  
            ),
            x=0.5,  
            y=0.9,  
            xanchor='center',  
            yanchor='top',  
         ),
        plot_bgcolor='white', 
        xaxis_showgrid=False,  
        yaxis_showgrid=True,  #
        yaxis_gridcolor="rgba(0,0,0,0.05)",  
        font=dict(
            family="'Poppins', sans-serif"  
        ),
        width=550, 
        height=350,
        legend=dict(
            orientation='h',  
            y=0.95,  
            x=0.5,   
            xanchor='center', 
            yanchor='bottom',  
            traceorder="normal"  
        )
    )

    fig = go.Figure(data=data, layout=layout)

    chart_html = pio.to_html(fig, full_html=False)

    return chart_html


def create_horizontal_bar_chart(leadership_diversity, demographic_breakdown):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[leadership_diversity],
        y=['Leadership'],
        name='Leadership',
        orientation='h',  
        marker=dict(color='#fad9c7'),
        width=0.2
    ))
    fig.add_trace(go.Bar(
        x=[0] * len(demographic_breakdown),
        y=demographic_breakdown,
        name='Diversity Breakdown',
        orientation='h',  
        marker=dict(color='#F07837'),
        width=0.2
    ))

    # Layout
    fig.update_layout(
        title=dict(
            text='Diversity in Leadership Positions',
            font=dict(
                family="'Poppins', sans-serif", 
                size=20,  
            ),
            x=0.5,  
            y=0.9,  
            xanchor='center',  
            yanchor='top',  
        ),
        barmode='group',
        width=600,  
        height=400, 
        font=dict(
            family="'Poppins', sans-serif"  
        ),
        legend=dict(
            orientation='h',  
            yanchor='bottom',  
            y=1.02,  
            xanchor='center', 
            x=0.5  
        ),
        plot_bgcolor='white',  
        xaxis=dict(
            gridcolor='#f3f5f6',  
        ),
        yaxis=dict(
            gridcolor='#f3f5f6',  
        )
    )

    chart_html = pio.to_html(fig, full_html=False)

    return chart_html