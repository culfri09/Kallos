# Defines routes
from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
views = Blueprint('views', __name__)
from website.dash import create_radar_chart
import plotly.graph_objs as go
from plotly.offline import plot
import chart_studio.tools as tls
from website.dash import create_charts
from website.kpi import analyze_kpi


# Define route for the landing page
@views.route('/')
def landing_page():
    # If the user is authenticated, redirect them to the home page
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    # If the user is not authenticated, render the "hero page"
    return render_template("hero.html")

# Define route for the home page
@views.route('/home')
@login_required  # Ensure the user is logged in to access this page
def home():
    radar_chart_html, line_graph_html, gauge_chart_html, stacked_bar_chart_html,bar_chart_html, horizontal_bar_chart_html,ratings_number = create_charts()
    return render_template("home.html", radar_chart_html=radar_chart_html,line_graph_html=line_graph_html, gauge_chart_html=gauge_chart_html,stacked_bar_chart_html=stacked_bar_chart_html,bar_chart_html=bar_chart_html,horizontal_bar_chart_html=horizontal_bar_chart_html,ratings_number=ratings_number)

@views.route('/hero')
def hero_page():
    return render_template('hero.html')

@views.route('/recommendations')
def recommendations_page():
    return render_template('recommendations.html')

@views.route('/questions')
@login_required
def questions_page():
    return render_template('base_questions.html')

@views.route('/surveys')
@login_required
def surveys_page():
    return render_template('base_surveys.html')

@views.route('/privacy_policy')
def privacy_policy_page():
    return render_template('privacy_policy.html')

@views.route('/tutorial')
@login_required
def tutorial_page():
    return render_template('tutorial.html')

@views.route('/benchmarking')
@login_required
def benchmarking_page():
    return render_template('benchmarking.html')

@views.route('/analyze_kpi', methods=['GET'])
def analyze_kpi_endpoint():
    result = analyze_kpi()
    return jsonify(result)

