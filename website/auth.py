# Defines routes related to user authentication
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .import models
from .import init
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import re
from .import encryption 
from flask import Flask, jsonify
import psycopg2
from psycopg2 import OperationalError
from flask_sqlalchemy import SQLAlchemy



auth = Blueprint('auth', __name__)
key = encryption.generate_key()

# Route for user login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form_data = {'email': ''}  
    if request.method == 'POST':
        email_input = request.form.get('email')
        password = request.form.get('password')

        form_data['email'] = email_input  # Update form data with email value

        # Retrieve all users from the database
        users = models.User.query.all()
        for user in users:
            # Decrypt the email retrieved from the database
            decrypted_email = encryption.decrypt(user.email, key)  # Replace 'key' with your decryption key
            if decrypted_email == email_input:
                # If decrypted email matches the email provided by the user, proceed with authentication
                if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    # If password is incorrect, display error
                    flash('Incorrect password, try again', category='error')
                break  # Stop looping through users once a matching email is found
        else:
            # If no user with matching email is found, display error
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

            
            # Performs data checks
            if models.User.query.filter_by(email=email).first():
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
                encrypted_email = encryption.encrypt(email, key)
                hashed_password = generate_password_hash(password1)
                encrypted_first_name = encryption.encrypt(first_name, key)
                encrypted_company_name = encryption.encrypt(company_name, key)
                encrypted_job_title = encryption.encrypt(job_title, key)
                encrypted_department = encryption.encrypt(department, key)
                # If all data is OK, create a new user
                data = {
                    'email': encrypted_email,
                    'password': hashed_password,
                    'first_name': encrypted_first_name,
                    'company_name': encrypted_company_name,
                    'job_title': encrypted_job_title,
                    'department': encrypted_department
                }

                # Create a new KallosUser object with the provided data
                new_user = models.User(**data)

                # Add the new_user to the database session
                init.db.session.add(new_user)

                # Commit the session to save the changes to the database
                init.db.session.commit()

                login_user(new_user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('views.home'))
                

            '''
                # If all data is OK, create a new user
                new_user = models.User(email=email, first_name=first_name, company_name=company_name,
                                        job_title=job_title, department=department,
                                        password=generate_password_hash(password1, method='pbkdf2:sha256'))            

                init.db.session.add(new_user)
                init.db.session.commit()

                # Logs in user and loads homepage
                login_user(new_user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('views.home'))
            

            # Data to be inserted into the table
            data = {
                3,  # id
                email,  # email
                password1,  # password
                first_name,  # first_name
                company_name,  # company_name
                job_title,  # job_title
                department  # department
            }
            print(data)'''

            

        # Loads sign up page
        return render_template("sign_up.html", form_data=form_data) 
    
    except Exception as e:
        # Exception handling: display error
        error_message = "An error occurred while processing your request: {}".format(str(e))
        return jsonify({"error": error_message}), 500