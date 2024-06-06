"""
This module analyzes the company's KPI.
"""
from flask_login import current_user
from . import models
from openai import OpenAI


def analyze_kpi():
    """
    Function to analyze and calculate the employer brand score based data.
    """

    employer_branding_metrics = {}  

    #Fetches data from database
    if current_user.is_authenticated:
        user_id = current_user.id
        user_scrapes = models.Scraping.query.filter_by(kallosusers_id=user_id).first()
        user_surveys = models.Surveys.query.filter_by(kallosusers_id=user_id).first()
        user_answers = models.Answers.query.filter_by(kallosusers_id=user_id).first()

        if user_scrapes:
            worklife_balance_rating = user_scrapes.worklife_balance_rating
            salary_rating = user_scrapes.salary_rating
            work_stability_rating = user_scrapes.work_stability_rating
            management_rating = user_scrapes.management_rating
            work_culture_rating = user_scrapes.work_culture_rating
            ratings_number = user_scrapes.ratings_number

            employer_branding_metrics.update({
                'Worklife Balance': worklife_balance_rating,
                'Salary': salary_rating,
                'Work Stability': work_stability_rating,
                'Management': management_rating,
                'Work Culture': work_culture_rating,
                'Ratings': ratings_number
            })

        if user_surveys:
            enps = user_surveys.enps
            candidate_rate = user_surveys.candidate_rate
            retention_rate = user_surveys.retention_rate
            workplace_rate = user_surveys.workplace_rate

            employer_branding_metrics.update({
                'Enps': enps,
                'Candidate Rate': candidate_rate,
                'Retention Rate': retention_rate,
                'Workplace Rate': workplace_rate
            })

        if user_answers:
            development = user_answers.development
            demographic = user_answers.demographic_breakdown
            leadership_diversity = user_answers.leadership_diversity
            familiarity = user_answers.employer_brand_familiarity
            channels = user_answers.channels
            investment = user_answers.investment

            employer_branding_metrics.update({
                'Development': development,
                'Demographic': demographic,
                'Leadership diversity': leadership_diversity,
                'Employer Branding Familiarity': familiarity,
                'Recruitment Channels': channels,
                'Investment': investment
            })
    
    # Initializes LLM conection and performs analysis
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    answer = 'I want you to calculate the employer brand score of this company based on the following metrics:' + str(employer_branding_metrics)
    
    completion = client.chat.completions.create(
        model="QuantFactory/Meta-Llama-3-8B-Instruct-GGUF",
        messages=[
            {"role": "system", "content": "You are an objective assistant. You only provide numbers (scores) as answers. Scores should be from 1-100. "},
            {"role": "user", "content": answer}
        ],
        temperature=0.7,
    )

    # Extracts the KPI from the API response
    kpi = completion.choices[0].message.content
    return {"kpi": kpi}
