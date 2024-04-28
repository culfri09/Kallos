from flask import Flask, render_template, request, redirect, url_for
from .import init
from datetime import datetime
from .import models
from flask_login import current_user
from flask import Blueprint

submissions = Blueprint('submissions', __name__)

@submissions.route('/answers_submission', methods=['POST'])
def submit_answers():
    # Extracts form data
    benchmark_companies = request.form['benchmarkCompanies']
    time_to_fill = request.form['timeToFill']
    demographic_breakdown = request.form['demographicBreakdown']
    leadership_diversity = request.form['leadershipDiversity']
    net_promoter_score = request.form['NPS']
    employer_brand_familiarity = request.form['brandFamiliarity']
    
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

    return render_template("home.html")

