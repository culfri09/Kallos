# Defines routes
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
views = Blueprint('views', __name__)

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
    # Render the home page template
    return render_template("home.html")

@views.route('/hero')
def hero_page():
    return render_template('hero.html')
