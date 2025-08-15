from collections import Counter
import re
from flask import render_template, request
import pandas as pd

dataset_1 = pd.read_excel("dataset.xlsx")


def select(domain):
    
    filtered_jobs = dataset_1[dataset_1['Domain'] == domain]
    if filtered_jobs.empty:
        message = f"No jobs available for the domain: {domain}"
        jobs = []
    else:
        message = f"Jobs in {domain}"
        jobs = filtered_jobs.reset_index()[['index', 'Job', 'Domain']].to_dict(orient='records')
    return message,jobs

def specific():
    domain_input = request.form.get('domain_name').strip().lower()  # Get user input
    
    bracketed_keywords = set()
    for domain in dataset_1['Domain']:
        matches = re.findall(r'\((.*?)\)', domain)
        bracketed_keywords.update(match.lower() for match in matches)
    
    if domain_input in ['ai', 'artificial intelligence']:
        print(dataset_1['Domain'].str.lower())
        filtered_jobs = dataset_1[dataset_1['Domain'].str.lower() == 'artificial intelligence (ai)']

    elif domain_input == 'iot':
        filtered_jobs = dataset_1[dataset_1['Domain'].str.contains(r'Internet of Things \(IoT\)', na=False, case=False)]
    elif domain_input in bracketed_keywords:
        pattern = f"\\({domain_input.upper()}\\)"
        
        filtered_jobs = dataset_1[dataset_1['Domain'].str.contains(pattern, na=False)]
    else:
        filtered_jobs = dataset_1[dataset_1['Domain'].str.lower().str.contains(domain_input, na=False)]
    
    if filtered_jobs.empty:
        message = f"No jobs found for the domain: {domain_input.capitalize()}"
        jobs = []
    else:
        message = f"Jobs in {domain_input.capitalize()}:"
        jobs = filtered_jobs.reset_index()[['index', 'Job', 'Domain']].to_dict(orient='records')

    return message, jobs

def filter(job_title):
    filtered_jobs =  dataset_1[dataset_1['Job'].str.contains(job_title, case=False, na=False)]

    if filtered_jobs.empty:
        message = f"No matching jobs found for: {job_title}"
        jobs = []
    else:
        # Matches found
        message = f"Matching Jobs for '{job_title}':"
        jobs = filtered_jobs.reset_index()[['index', 'Job', 'Domain']].to_dict(orient='records')
    
    return message,jobs

def specific_skill(skills):

    skills = [skill.strip().lower() for skill in skills]
    
    # Filter jobs where at least 3 skills match
    matching_jobs = dataset_1[dataset_1["Skills Required"].apply(
        lambda x: sum(skill in str(x).lower() for skill in skills) >= 3
    )]
    
    if matching_jobs.empty:
        message = "No jobs found that match at least 3 of the provided skills."
        jobs = []
    else:
        message = "Jobs matching your skills:"
        jobs = matching_jobs.reset_index()[['index', 'Job', 'Domain']].to_dict(orient='records')
    
    return message, jobs

def get_salary_options():
    # Count occurrences of each salary range
    salary_counts = Counter(dataset_1["Salary (₹ LPA)"])
    
    # Filter for salary ranges with counts greater than or equal to 5
    filtered_salaries = {salary_range: count for salary_range, count in salary_counts.items() if count >= 5}
    
    # Add a placeholder option for the dropdown without a job count
    options = {"Select by Salary": None}  # Placeholder option with no job count
    options.update(filtered_salaries)
    
    return options


def select_salary_get(selected_salary):
    filtered_jobs = dataset_1[dataset_1['Salary (₹ LPA)'] == selected_salary]

    if filtered_jobs.empty:
        message = f"No matching jobs found for the salary range: {selected_salary}"
        jobs = []
    else:
        message = f"Matching Jobs for '{selected_salary}':"
        jobs = filtered_jobs.reset_index()[['index', 'Job', 'Domain']].to_dict(orient='records')

    return message, jobs