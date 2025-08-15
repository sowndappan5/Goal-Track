import re
import os
import hashlib
import json
import google.generativeai as genai
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Set your Gemini API key - in production, use environment variables
GEMINI_API_KEY = "AIzaSyB335UzzSBBxHj94igOEAThkn_G_uFP9UY"
genai.configure(api_key=GEMINI_API_KEY)

# Cache to store previously generated assessments
assessment_cache = {}

EXCEL_PATH = 'marks.xlsx'  # Path to your Excel file

assessment_cache = {}

def extract_day_blocks(md_content):
    """
    Extract day blocks from the markdown content.
    Expected to match patterns like "### Day 1:" and end with a separator line '---'.
    Returns a list of tuples: (day_number, block_content).
    """
    pattern = r'### Day (\d+):\s*(.*?)\n---'
    matches = re.findall(pattern, md_content, re.DOTALL)
    day_blocks = []
    for day_str, block in matches:
        try:
            day = int(day_str)
            day_blocks.append((day, block.strip()))
        except ValueError:
            continue
    print("day blocks --------------------")
    return day_blocks

def filter_content_by_day(md_content, input_day):
    """
    Splits the markdown content into sections using the separator line.
    Each section is expected to start with a header "### Day X:".
    A section with no content after the header is considered a group boundary.
    
    For example:
      - If input_day is 7, we return content for days 1–6.
      - If input_day is 14, we identify that Day 7 is empty (group boundary)
        and then return sections for days 8–13.
    """

    # Split on the separator line
    sections = extract_day_blocks(md_content)
    day_sections = []
    # Extract the day number and the content of each section
    for sec in sections:
        match = re.search(r'### Day (\d+):(.*)', sec, re.DOTALL)
        if match:
            day_num = int(match.group(1))
            content_after_header = match.group(2).strip()
            day_sections.append((day_num, sec.strip()))
    
    # Determine the previous boundary:
    # a section with an empty header content is our group separator.
    previous_boundary = 0
    for day, sec in day_sections:
        match = re.search(r'### Day \d+:(.*)', sec, re.DOTALL)
        if match:
            content_after_header = match.group(1).strip()
            if day < input_day and content_after_header == "":
                previous_boundary = day
    
    start_day = previous_boundary + 1 if previous_boundary else 1
    # Filter sections that fall within start_day (inclusive) and input_day (exclusive)
    filtered_sections = [sec for day, sec in day_sections if start_day <= day < input_day]
    print("-------------------------------------------------------------")
    print(filtered_sections)
    return "\n\n".join(filtered_sections)

def generate_assessment_from_content(content):
    """Generate assessment questions using Gemini AI based on task.md content"""
    content_hash = hashlib.md5(content.encode()).hexdigest()
    if content_hash in assessment_cache:
        return assessment_cache[content_hash]
    
    print(content)

    prompt = f"""
    You are an expert educator creating an assessment.

    Please read the following content topics:

    {content}

    Based on this content, create exactly 10 multiple-choice questions to test understanding of these concepts.

    For each question:
    1. Create a clear, specific question related to the content
    2. Provide 4 options (a, b, c, d)
    3. Mark the correct answer with [CORRECT]
    4. Make sure distractors (wrong answers) are plausible

    Format your response as JSON with this structure:
    {{
        "questions": [
            {{
                "question": "Question text goes here?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correctAnswerIndex": 2
            }},
            ...more questions...
        ]
    }}

    Only return the JSON data. Do not include any other text or explanation.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        print("Gemini Response:", response.text)
        json_text = response.text
        # Remove code block markers if present
        json_text = re.sub(r'```(json)?', '', json_text).strip()
        
        if json_text:
            assessment_data = json.loads(json_text)
        else:
            raise ValueError("Gemini returned an empty JSON string after removing code markers.")
        
        assessment_cache[content_hash] = assessment_data
        return assessment_data

    except Exception as e:
        print(f"Error generating assessment: {e}")
        # Return a fallback assessment if Gemini fails
        return {
            "questions": [
                {
                    "question": "What is the primary cryptographic hash function used in Bitcoin?",
                    "options": ["MD5", "SHA-1", "SHA-256", "SHA-512"],
                    "correctAnswerIndex": 2
                },
                {
                    "question": "What is a key advantage of Elliptic Curve Cryptography compared to RSA?",
                    "options": [
                        "It requires larger key sizes",
                        "It provides equivalent security with smaller key sizes",
                        "It's easier to implement",
                        "It was invented more recently"
                    ],
                    "correctAnswerIndex": 1
                }
                # Additional fallback questions could be added here
            ]
        }

@app.route('/')
def index():
    return render_template('assessment3.html')

@app.route('/get_assessment', methods=['GET'])
def build_assessment():
    try:
        with open('task.md', 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
        assessment_data = generate_assessment_from_content(content)

        print(assessment_data)
        # Remove correctAnswerIndex before sending to frontend
        frontend_data = {"questions": []}
        for q in assessment_data["questions"]:
            options = [re.sub(r'\[CORRECT\]', '', opt).strip() for opt in q["options"]]
            frontend_data["questions"].append({
                "question": q["question"],
                "options": options
            })
        return jsonify({"success": True, "assessment": frontend_data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

def update_excel(username, day, score):
    """
    Update the Excel file with the score for the appropriate assessment.
    The mapping is as follows:
      - Day 7  → 'assessment 1'
      - Day 14 → 'assessment 2'
      - Day 21 → 'assessment 3'
      - Day 28 → 'assessment 4'
      - Day 35 → 'assessment 5'
    """
    mapping = {7: 'assessment 1', 14: 'assessment 2', 21: 'assessment 3', 28: 'assessment 4', 30: 'assessment 5'}
    column = mapping.get(day)
    if not column:
        print("Day value does not map to any assessment column")
        return

    try:
        # Load existing Excel file or create a new DataFrame with the proper columns
        if os.path.exists(EXCEL_PATH):
            df = pd.read_excel(EXCEL_PATH)
        else:
            df = pd.DataFrame(columns=['username', 'assessment 1', 'assessment 2', 'assessment 3', 'assessment 4', 'assessment 5'])
        
        print("DataFrame before updating:")
        print(df)
        
        # Update the row if the username exists; otherwise, add a new row.
        if username in df['username'].values:
            df.loc[df['username'] == username, column] = score
        else:
            new_row = {'username': username, column: score}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
        print("DataFrame after updating:")
        print(df)
        
        # Save the updated DataFrame back to Excel
        df.to_excel(EXCEL_PATH, index=False)
        print(f"Updated {username}'s {column} with score {score}")
    except Exception as e:
        print(f"Error updating Excel file: {e}")
        
@app.route('/submit_assessment', methods=['POST'])
def submit_assessment():
    try:
        data = request.json
        if not data or 'answers' not in data:
            return jsonify({"success": False, "error": "Missing answers data"}), 400
        
        # Remove and convert 'day' parameter
        day_value = data.pop('day', None)
        if day_value is None:
            return jsonify({"success": False, "error": "Missing day parameter"}), 400
        
        try:
            day_value = int(day_value)
        except ValueError:
            return jsonify({"success": False, "error": "Invalid day parameter"}), 400

        # Use default username without reading input
        username = "default_user"

        user_answers = data.get('answers', [])
        print("User Answers:", user_answers)
        print("Day value:", day_value)
        print("Username:", username)

        # Read the task.md content
        with open('task.md', 'r', encoding='utf-8') as file:
            content = file.read()

        # Generate the assessment (uses caching if available)
        assessment_data = generate_assessment_from_content(content)
        questions = assessment_data["questions"]

        # Calculate the score based on correctAnswerIndex for each question
        score = 0
        results = []
        for i, (q, user_ans) in enumerate(zip(questions, user_answers)):
            correct_ans = q["correctAnswerIndex"]
            is_correct = user_ans == correct_ans
            if is_correct:
                score += 1
            results.append({
                "question": i,
                "correct": is_correct,
                "userAnswer": user_ans,
                "correctAnswer": correct_ans,
                "explanation": f"The correct answer is: {q['options'][correct_ans]}"
            })

        # Update Excel file using the default username
        update_excel(username, day_value, score)

        return jsonify({
            "success": True,
            "score": score,
            "total": len(questions),
            "results": results
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True)
