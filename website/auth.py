# Defines routes related to user authentication
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .import models
from .import init
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import re


auth = Blueprint('auth', __name__)

# Route for user login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form_data = {'email': ''}  # Initialize form data outside the conditional block
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        form_data['email'] = email  # Update form data with email value

        user = models.User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", form_data=form_data)

# Route for user logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Route for user sign-up
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form_data = {}  # Initialize empty form data

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        company_name = request.form.get('companyName')
        job_title = request.form.get('jobTitle')
        department = request.form.get('department')

        form_data = {
            'email': email,
            'first_name': first_name,
            'company_name': company_name,
            'job_title': job_title,
            'department': department
        }

        user = models.User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Passwords must be at least 7 characters', category='error')
        elif not any(char.isupper() for char in password1):
            flash('Password must contain at least 1 capital letter', category='error')
        elif not any(char.isdigit() for char in password1):
            flash('Password must contain at least 1 digit', category='error')
        elif not re.search(r'[!@#$%^&*()_+={}\[\]:;"\'|<,>.?/~`]$', password1):
            flash('Password must contain at least 1 special character', category='error')
        else:
            new_user = models.User(email=email, first_name=first_name, company_name=company_name,
                                    job_title=job_title, department=department,
                                    password=generate_password_hash(password1, method='pbkdf2:sha256'))
            init.db.session.add(new_user)
            init.db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", form_data=form_data) 