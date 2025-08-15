from flask import render_template, request
import pandas as pd

df = pd.read_excel('course.xlsx')

def course_get(salary_options):
    topics = []
    
    for topic in df['Topic'].unique():
        subtopics = df[df['Topic'] == topic]['Subtopic'].tolist()
        topics.append({
            'Topic': topic,
            'Subtopics': subtopics
        })

    return render_template('home.html', topics=topics, salary_options=salary_options) # Give course list

def subtopic_get(subtopic_name):
    # Filter data based on the selected subtopic
    subtopic_data = df[df['Subtopic'] == subtopic_name].iloc[0]
    
    if request.method == 'POST':
        selected_course = request.form['selected_course']
        return render_template('course_info.html',
                               topic=subtopic_data['Topic'],
                               subtopic=subtopic_data['Subtopic'],
                               description=subtopic_data['Description'],
                               selected_course=selected_course)
    
    return render_template('job_details.html', 
                           topic=subtopic_data['Topic'], 
                           subtopic=subtopic_data['Subtopic'],
                           contents=subtopic_data['Contents'],
                           image=subtopic_data['Image'],
                           description=subtopic_data['Description']) # give course info