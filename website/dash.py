import plotly.graph_objs as go

# Data
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
data = [go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself',
    name='Ratings'
)]

# Layout
layout = go.Layout(
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

# Creating figure
fig = go.Figure(data=data, layout=layout)

# Displaying dashboard
fig.show()
