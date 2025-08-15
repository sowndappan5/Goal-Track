from flask import Flask, jsonify, render_template, send_from_directory
import pandas as pd
import os

from leaderboard import leaderboard

app = Flask(__name__, static_folder='static', template_folder='templates')


def get_assessment_data():
    try:
        # Use the correct file path
        file_path = "marks.xlsx"

        # Check if file exists
        if not os.path.exists(file_path):
            print("Error: File not found")
            return jsonify({'error': 'File not found'}), 404

        # Read the Excel file
        df = pd.read_excel(file_path)

        # Print the first few rows to debug
        print("Excel Data:\n", df.head())

        # Check if 'username' column exists
        if 'username' not in df.columns:
            print("Error: 'username' column missing")
            return jsonify({'error': "The 'username' column is missing"}), 400

        # Extract users and assessments
        users = df['username'].tolist()
        assessments = [col for col in df.columns if col != 'username']

        # Prepare JSON data
        data = {'users': users, 'assessments': assessments, 'scores': {}}
        for user in users:
            user_data = df[df['username'] == user]
            data['scores'][user] = user_data[assessments].values.tolist()[0]

        return jsonify(data)

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
