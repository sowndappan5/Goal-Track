from flask import Flask, jsonify, render_template, request
import re
from assessment4 import build_assessment, extract_day_blocks, filter_content_by_day, generate_assessment_from_content, submit_assessment
from analyze import fetch_notes, json_to_text, analyze_notes, save_to_markdown


app = Flask(__name__)

def parse_tasks():
    with open("task.md", "r", encoding="utf-8") as file:
        content = file.read()

    tasks = []
    headers = re.findall(r'\*\*\*(.+?)\*\*\*', content)  # Extract section headers
    day_blocks = re.split(r'### Day (\d+): (.+)', content)[1:]
    current_header = headers[0] if headers else "No Section"
    parsed_days = {}

    for i in range(0, len(day_blocks), 3):
        day_number = int(day_blocks[i])
        title = day_blocks[i+1]
        details = day_blocks[i+2].strip()

        # Check if there's a new section header before this day
        new_header_match = re.search(r'\*\*\*(.+?)\*\*\*', details)
        if new_header_match:
            current_header = new_header_match.group(1)

        # Extract topics
        topics_match = re.search(r'## Topics:\n([\s\S]+?)\n\n🎯 Tasks:', details)
        topics = [line.strip() for line in topics_match.group(1).split("\n") if line.strip()] if topics_match else []

        # Extract tasks as checkboxes
        tasks_match = re.findall(r'✅ (.+)', details)
        tasks_data = [{"task": t, "completed": False} for t in tasks_match]

        parsed_days[day_number] = {
            "day": day_number,
            "head": current_header,
            "subhead": f"Day {day_number}: {title}",
            "topics": topics,
            "tasks": tasks_data
        }

    # Fill in missing days (assuming a 30-day plan)
    max_day = 30
    for day in range(1, max_day + 1):
        if day not in parsed_days:
            parsed_days[day] = {
                "day": day,
                "head": "Assessment",
                "subhead": f"Day {day}: Take Assessment",
                "topics": [],
                "tasks": []  # No tasks means it's an assessment day
            }

    # Return a sorted list of tasks by day number
    return [parsed_days[day] for day in sorted(parsed_days)]

notes = []  # Store notes as a list

notes = []

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/save_note', methods=['POST'])
def save_note():
    data = request.get_json()
    note_text = data.get("note")

    if not note_text:
        return jsonify({"error": "Empty note"}), 400

    day_number = len(notes) + 1  # Assign day count
    notes.append({"day": f"Day {day_number}", "note": note_text})

    return jsonify({"message": "Note saved!", "day": f"Day {day_number}"}), 201

@app.route('/get_notes', methods=['GET'])
def get_notes():
    return jsonify(notes)


@app.route('/analyze_notes', methods=['GET'])
def analyze():
    notes_data = fetch_notes()  # Fetch stored notes
    if "error" in notes_data:
        return jsonify({"error": notes_data["error"]}), 500

    formatted_text = json_to_text(notes_data)  # Convert JSON to text
    analysis_result = analyze_notes(formatted_text)  # Analyze notes

    # Save analysis to markdown (optional)
    markdown_content = f"## Analysis\n\n{analysis_result}\n"
    save_to_markdown(markdown_content)

    return {"analysis": analysis_result}


@app.route('/tasks')
def get_tasks():
    return jsonify(parse_tasks())

@app.route('/get_assessment')
def get_assessment():
    return build_assessment()

@app.route('/assessment4.html')
def assessment_page():
    return render_template("assessment4.html")

@app.route('/submit_assessment', methods=['POST'])
def sub():
    return submit_assessment()


if __name__ == '__main__':
    app.run(debug=True)
