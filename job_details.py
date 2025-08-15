from flask import render_template
import pandas as pd

dataset_1 = pd.read_excel("dataset.xlsx")

def job_details_get(job_id):
    try:
        job = dataset_1.loc[int(job_id)]  
        job_details = get_job_details(job) 
        return render_template('job_details.html', job_details=job_details) # give job info
    except (KeyError, ValueError):
        return "Job not found", 404

def get_job_details(job):
    """Extract job details as a dictionary."""
    return {key: job[key] for key in job.index}