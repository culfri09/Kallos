from flask import Flask, render_template, request, redirect, url_for, flash
from .import init
from datetime import datetime
from .import models
from flask import Blueprint
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import PyPDF2
from flask import current_app
from openai import OpenAI
from website.web_scraping import scrape

submissions = Blueprint('submissions', __name__)

'''ANSWERS SUBMISSION'''
@submissions.route('/answers_submission', methods=['POST'])
def submit_answers():
    # Extracts form data
    benchmark_companies = request.form.get('benchmarkCompanies') or None
    demographic_breakdown = request.form.get('demographicBreakdown') or None
    leadership_diversity = request.form.get('leadershipDiversity') or None
    employer_brand_familiarity = request.form.get('brandFamiliarity') or None
    channels = request.form.get('channels') or None
    investment = request.form.get('investment') or None
    development = request.form.get('development') or None

    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    answer = development + 'Imagine this is the answer of a company to the initiatives they have for development. How effective are their initiatives? Only write percentage. No more text. Only 1 word with percentage of result '
    completion = client.chat.completions.create(
        model="QuantFactory/Meta-Llama-3-8B-Instruct-GGUF",
        messages=[
            {"role": "system", "content": "You are an objective assistant. Please evaluate the effectiveness of the initiatives mentioned. You only provide percentages as answers"},
            {"role": "user", "content": answer}
        ],
        temperature=0.7,
    )

    development_metric=completion.choices[0].message.content

    # Gets the ID of the currently logged-in user
    user_id = current_user.id

    # Creates a new instance of Answers model
    new_answer = models.Answers(
        kallosusers_id=user_id,
        benchmark_companies=benchmark_companies,
        demographic_breakdown=demographic_breakdown,
        leadership_diversity=leadership_diversity,
        employer_brand_familiarity=employer_brand_familiarity,
        timestamp=datetime.now(),
        channels=channels,
        investment=investment,
        development=development_metric
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
        demographic_breakdown = request.form['demographicBreakdown']
        leadership_diversity = request.form['leadershipDiversity']
        employer_brand_familiarity = request.form['brandFamiliarity']
        channels = request.form['channels']
        investment = request.form['investment']
        development = request.form['development']

        # Gets the ID of the currently logged-in user
        user_id = current_user.id

        # Querys existing answer record for the current user
        existing_answer = models.Answers.query.filter_by(kallosusers_id=user_id).first()

        if existing_answer:
            # Updates existing record with new values
            existing_answer.benchmark_companies = benchmark_companies if benchmark_companies else existing_answer.benchmark_companies
            existing_answer.demographic_breakdown = demographic_breakdown if demographic_breakdown else existing_answer.demographic_breakdown
            existing_answer.leadership_diversity = leadership_diversity if leadership_diversity else existing_answer.leadership_diversity
            existing_answer.employer_brand_familiarity = employer_brand_familiarity if employer_brand_familiarity else existing_answer.employer_brand_familiarity
            existing_answer.channels = channels if channels else existing_answer.channels
            existing_answer.investment = investment if investment else existing_answer.investment
            existing_answer.development = development if development else existing_answer.development
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

        npsMetric = request.form.get('npsMetric')
        candidateMetric = request.form.get('candidateMetric')
        retentionMetric = request.form.get('retentionMetric')
        workplaceEnvironmentMetric = request.form.get('workplaceEnvironmentMetric')

        # Gets the ID of the currently logged-in user
        user_id = current_user.id

        # Validates the metrics
        enps = npsMetric if npsMetric else None
        candidate_rate = candidateMetric if candidateMetric else None
        retention_rate = retentionMetric if retentionMetric else None
        workplace_rate = workplaceEnvironmentMetric if workplaceEnvironmentMetric else None

        # Create or update the Surveys model with the analyzed data
        existing_survey = init.db.session.query(models.Surveys).filter_by(kallosusers_id=user_id).first()

        if existing_survey:
            # Update the existing survey with new data if provided
            if enps:
                existing_survey.enps = enps
            if candidate_rate:
                existing_survey.candidate_rate = candidate_rate
            if retention_rate:
                existing_survey.retention_rate = retention_rate
            if workplace_rate:
                existing_survey.workplace_rate = workplace_rate
            existing_survey.timestamp = datetime.now()
        else:
            # Create a new instance of Surveys model with the analyzed data
            new_survey = models.Surveys(
                kallosusers_id=user_id,
                enps=enps,
                candidate_rate=candidate_rate,
                retention_rate=retention_rate,
                workplace_rate=workplace_rate,
                timestamp=datetime.now(),
            )
            # Add the new_survey to the database session
            init.db.session.add(new_survey)
            
            # Commit changes to the database
            init.db.session.commit()
        # Dictionary to store survey data for each file field name
        survey_data = {}

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
                if file_extension == 'pdf':
                    # The file is allowed, save it to the UPLOAD_FOLDER
                    filename = secure_filename(file.filename)
                    #file.save(os.path.join(init.app.config['UPLOAD_FOLDER'], filename))
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    # Extract text data from PDF
                    text_data = extract_text_from_pdf(file_path)
                    # Add survey data to the dictionary
                    survey_data[file_field_name] = text_data
                else:
                    # The file has an invalid extension or format
                    flash(f'Invalid file for {survey_name}. Please upload a PDF file.', 'error')
                    upload_failed = True

        # If any file upload fails, render the same page with an error message
        if upload_failed:
            return render_template("base_surveys.html", error="File upload failed. Please try again.")

        # Call analyze_surveys function with all survey data
        analyze_surveys(survey_data)
        user_id = current_user.id
        scrape(user_id)
        return redirect(url_for('views.home'))

    # If GET request, render the form page for file upload
    return render_template("base_surveys.html")

def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text.strip()

def analyze_surveys(survey_data):
    # Point to the local server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    # Initialize variables to store survey results
    enps = candidate_rate = retention_rate = workplace_rate = None

    # Loop through each survey data
    for file_field_name, text_data in survey_data.items():
        # Process surveys based on file field name
        if file_field_name == 'npsSurvey':
            text_data += 'Calculate average nps. Only write number from 0 to 10. No more text. Only 1 word with number of result.'
            completion = client.chat.completions.create(
                model="QuantFactory/Meta-Llama-3-8B-Instruct-GGUF",
                messages=[
                    {"role": "system", "content": "You are an intelligent assistant. You always provide numbers as answers."},
                    {"role": "user", "content": text_data}
                ],
                temperature=0.7,
            )
            enps = completion.choices[0].message.content
        elif file_field_name == 'candidateExperienceRating':
            text_data += 'Calculate average candidate experience rating. Calculate average candidate experience rating. Only write number from 0 to 10. No more text. Only 1 word with number of result.'
            completion = client.chat.completions.create(
                model="QuantFactory/Meta-Llama-3-8B-Instruct-GGUF",
                messages=[
                    {"role": "system", "content": "You are an intelligent assistant. You always provide numbers as answers."},
                    {"role": "user", "content": text_data}
                ],
                temperature=0.7,
            )
            candidate_rate = completion.choices[0].message.content
        elif file_field_name == 'retentionSurvey':
            text_data += 'Calculate average retention rate. Only write number from 0 to 10. No more text. Only 1 word with number of result.'
            completion = client.chat.completions.create(
                model="QuantFactory/Meta-Llama-3-8B-Instruct-GGUF",
                messages=[
                    {"role": "system", "content": "You are an intelligent assistant. You always provide numbers as answers."},
                    {"role": "user", "content": text_data}
                ],
                temperature=0.7,
            )
            retention_rate = completion.choices[0].message.content
        elif file_field_name == 'workplaceEnviornmentSurvey':
            text_data += 'Calculate average workplace environment rate. Only write number from 0 to 10. No more text. Only 1 word with number of result.'
            completion = client.chat.completions.create(
                model="QuantFactory/Meta-Llama-3-8B-Instruct-GGUF",
                messages=[
                    {"role": "system", "content": "You are an intelligent assistant. You always provide numbers as answers."},
                    {"role": "user", "content": text_data}
                ],
                temperature=0.7,
            )
            workplace_rate = completion.choices[0].message.content
    
    # Gets the ID of the currently logged-in user
    user_id = current_user.id

    # Query the database to find an existing survey for the user
    existing_survey = init.db.session.query(models.Surveys).filter_by(kallosusers_id=user_id).first()

    if existing_survey:
        # Update the existing survey with new data
        if enps is not None:
            existing_survey.enps = enps
        if candidate_rate is not None:
            existing_survey.candidate_rate = candidate_rate
        if retention_rate is not None:
            existing_survey.retention_rate = retention_rate
        if workplace_rate is not None:
            existing_survey.workplace_rate = workplace_rate
        existing_survey.timestamp = datetime.now()
    else:
        # Create a new instance of Surveys model with the analyzed data
        new_survey = models.Surveys(
            kallosusers_id=user_id,
            enps=enps,
            candidate_rate=candidate_rate,
            retention_rate=retention_rate,
            workplace_rate=workplace_rate,
            timestamp=datetime.now(),
        )
        # Add the new_survey to the database session
        init.db.session.add(new_survey)

    # Commit changes to the database
    init.db.session.commit()
