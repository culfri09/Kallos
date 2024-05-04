"""
This module handles user authentication
"""
import re
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from . import models, init, encryption


auth = Blueprint('auth', __name__)
key = encryption.generate_key()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    form_data = {'email': ''}
    if request.method == 'POST':
        email_input = request.form.get('email')
        password = request.form.get('password')

        form_data['email'] = email_input  # Update form data with email value

        # Retrieve all users from the database
        users = models.User.query.all()
        for user in users:
            if user.email == email_input:
                # If emails match proceed with authentication
                if check_password_hash(user.password, password):
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

@auth.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    # Logs out the user and loads login page
    logout_user()
    return render_template("hero.html")

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """Handle user sign-up."""
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
                hashed_password = generate_password_hash(password1)
                encrypted_first_name = encryption.encrypt(first_name, key)
                encrypted_company_name = encryption.encrypt(company_name, key)
                encrypted_job_title = encryption.encrypt(job_title, key)
                encrypted_department = encryption.encrypt(department, key)

                # If all data is OK, create a new user
                data = {
                    'email': email,
                    'password': hashed_password,
                    'first_name': encrypted_first_name,
                    'company_name': encrypted_company_name,
                    'job_title': encrypted_job_title,
                    'department': encrypted_department
                }

                # Creates a new Kallos User object with the provided data
                new_user = models.User(**data)

                # Adds the new_user to the database session
                init.db.session.add(new_user)

                # Commits the session to save the changes to the database
                init.db.session.commit()

                # Writes encryption key to file
                write_encryption_key_to_file(key, new_user.id)

                login_user(new_user, remember=True)
                return render_template("tutorial.html")

        # Loads sign up page
        return render_template("sign_up.html", form_data=form_data)

    except Exception as e:
        # Exception handling: display error
        error_message = f"An error occurred while processing your request: {str(e)}"
        return jsonify({"error": error_message}), 500


def write_encryption_key_to_file(key, id):
    """Write encryption keys to txt file."""
    # Defines the filename
    filename = ".misc.txt"

    # Generates a timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Writes encryption key to file
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"ID: {id},Encryption Key: {key}, Timestamp: {timestamp}\n")
