# Defines routes related to user authentication
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .import models
from .import init
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import re
from .import encryption 
from flask import Flask, jsonify


auth = Blueprint('auth', __name__)

# Route for user login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form_data = {'email': ''}  
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        form_data['email'] = email  # Update form data with email value

        # If user is found 
        user = models.User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                # If credentials are correct, load homepage
                return redirect(url_for('views.home'))
            else:
                # If credentials are incorrect, display error
                flash('Incorrect password, try again', category='error')
        else:
            # If user is not found, display error
            flash('Email does not exist', category='error')

    # Loads login page
    return render_template("login.html", form_data=form_data)

# Route for user logout
@auth.route('/logout')
@login_required
def logout():
    # Logs out the user and loads login page
    logout_user()
    return redirect(url_for('auth.login'))

# Route for user sign-up
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    try:
        form_data = {}  # Initializes empty form data

        # Gets data from signup form
        if request.method == 'POST':
            email = request.form.get('email')
            first_name = request.form.get('firstName')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')
            company_name = request.form.get('companyName')
            job_title = request.form.get('jobTitle')
            department = request.form.get('department')

            # Creates dictionary with form data
            form_data = {
                'email': email,
                'first_name': first_name,
                'company_name': company_name,
                'job_title': job_title,
                'department': department
            }

            # Creates dictionary for encrypted data
            data_encrypted = {
                'email': '',
                'first_name': '',
                'company_name': '',
                'job_title': '',
                'department': ''
            }

            user = models.User.query.filter_by(email=email).first()

            # Performs data checks
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
                try:
                    # If all data is OK
                    key = encryption.generate_key()
                    file_name = 'temp_data.txt'

                    with open(file_name, 'w') as file:
                        file.write(str(key))

                    # Encrypts all values in dictionary
                    for temp_key in form_data.keys():
                        data_encrypted[temp_key] = encryption.encrypt(data_encrypted[temp_key] , key)
                except:
                    pass
               
                # Adds encrypted data into database
                new_user = models.User(email=email, first_name=data_encrypted['first_name'], company_name=data_encrypted['company_name'],
                                        job_title=data_encrypted['job_title'], department=data_encrypted['department'],
                                        password=generate_password_hash(password1, method='pbkdf2:sha256'))            
            
                # Database connection and commit
                init.db.session.add(new_user)
                init.db.session.commit()
                # Logs in user and loads homepage
                login_user(new_user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('views.home'))

        # Loads sign up page
        return render_template("sign_up.html", form_data=form_data) 
    except Exception as e:
        # Exception handling: display error
        error_message = "An error occurred while processing your request: {}".format(str(e))
        return jsonify({"error": error_message}), 500