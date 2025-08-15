from flask import Flask
import re

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

if __name__ == '__main__':
    app.run(debug=True)
