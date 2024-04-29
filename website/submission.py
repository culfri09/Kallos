from flask import Flask, render_template, request, redirect, url_for, flash
from .import init
from datetime import datetime
from .import models
from flask import Blueprint
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

submissions = Blueprint('submissions', __name__)

'''ANSWERS SUBMISSION'''
@submissions.route('/answers_submission', methods=['POST'])
def submit_answers():
    # Extracts form data
    benchmark_companies = request.form.get('benchmarkCompanies') or None
    time_to_fill = request.form.get('timeToFill') or None
    demographic_breakdown = request.form.get('demographicBreakdown') or None
    leadership_diversity = request.form.get('leadershipDiversity') or None
    net_promoter_score = request.form.get('NPS') or None
    employer_brand_familiarity = request.form.get('brandFamiliarity') or None
    
    # Gets the ID of the currently logged-in user
    user_id = current_user.id

    # Creates a new instance of Answers model
    new_answer = models.Answers(
        kallosusers_id=user_id,
        benchmark_companies=benchmark_companies,
        time_to_fill=time_to_fill,
        demographic_breakdown=demographic_breakdown,
        leadership_diversity=leadership_diversity,
        net_promoter_score=net_promoter_score,
        employer_brand_familiarity=employer_brand_familiarity,
        timestamp=datetime.now()
    )

    # Adds the new_answer to the database session
    init.db.session.add(new_answer)

    # Commits the session to save the changes to the database
    init.db.session.commit()

    return render_template("base_surveys.html")

@submissions.route('/changed_answers_submission', methods=['POST'])
def submit_changed_answers():
# Extracts form data
        benchmark_companies = request.form['benchmarkCompanies']
        time_to_fill = request.form['timeToFill']
        demographic_breakdown = request.form['demographicBreakdown']
        leadership_diversity = request.form['leadershipDiversity']
        net_promoter_score = request.form['NPS']
        employer_brand_familiarity = request.form['brandFamiliarity']
        
        # Gets the ID of the currently logged-in user
        user_id = current_user.id

        # Querys existing answer record for the current user
        existing_answer = models.Answers.query.filter_by(kallosusers_id=user_id).first()

        if existing_answer:
            # Updates existing record with new values
            existing_answer.benchmark_companies = benchmark_companies if benchmark_companies else existing_answer.benchmark_companies
            existing_answer.time_to_fill = time_to_fill if time_to_fill else existing_answer.time_to_fill
            existing_answer.demographic_breakdown = demographic_breakdown if demographic_breakdown else existing_answer.demographic_breakdown
            existing_answer.leadership_diversity = leadership_diversity if leadership_diversity else existing_answer.leadership_diversity
            existing_answer.net_promoter_score = net_promoter_score if net_promoter_score else existing_answer.net_promoter_score
            existing_answer.employer_brand_familiarity = employer_brand_familiarity if employer_brand_familiarity else existing_answer.employer_brand_familiarity

        # Commits the session to save the changes to the database
        init.db.session.commit()

        return redirect(url_for('submissions.display_questions'))


@submissions.route('/bank_questions')
@login_required
def display_questions():
    # Fetches the user's answers from the database
    user_answers = models.Answers.query.filter_by(kallosusers_id=current_user.id).all()

    # Renders the questions.html template and pass the user's answers
    return render_template("questions.html", answers=user_answers)


'''SURVEYS SUBMISSIONS'''
@submissions.route('/surveys_upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Flag to track if any file upload fails
        upload_failed = False

        # Loop through each survey
        for survey_name, file_field_names in init.ALLOWED_EXTENSIONS.items():
            # Loop through each file upload field for the current survey
            for file_field_name in file_field_names:
                file = request.files[file_field_name]
                if file.filename == '':
                    # No file was selected for this survey, skip it
                    continue
                # Extract the file extension
                file_extension = file.filename.rsplit('.', 1)[1].lower()
                print(file_extension)
                if file_extension == 'pdf':
                    # The file is allowed, save it to the UPLOAD_FOLDER
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(init.app.config['UPLOAD_FOLDER'], filename))
                else:
                    # The file has an invalid extension or format
                    flash(f'Invalid file for {survey_name}. Please upload a PDF file.', 'error')
                    upload_failed = True

        # If any file upload fails, render the same page with an error message
        if upload_failed:
            return render_template("base_surveys.html", error="File upload failed. Please try again.")

        # Redirect to the home page after successful upload of all files
        return redirect(url_for('views.home'))

    # If GET request, render the form page for file upload
    return render_template("base_surveys.html")
