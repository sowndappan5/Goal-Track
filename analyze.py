import requests
import google.generativeai as genai

# Domain of learning
cc = "Blockchain"

# Configure Gemini API
GEMINI_API_KEY = "API"
genai.configure(api_key=GEMINI_API_KEY)

# Flask API Endpoints for fetching notes
api_urls = {
    "range1": "http://127.0.0.1:5000/combined_notes_range1",  # Day 1 to 6
    "range2": "http://127.0.0.1:5000/combined_notes_range2",  # Day 8 to 13
    "range3": "http://127.0.0.1:5000/combined_notes_range3",  # Day 15 to 20
    "range4": "http://127.0.0.1:5000/combined_notes_range4",  # Day 22 to 27
}

# Function to fetch notes from Flask API
def fetch_notes(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return json_to_text(data)  # Convert JSON to text
        else:
            return f"Error fetching data: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

# Function to convert JSON data to structured text
def json_to_text(data):
    notes_text = ""
    for key, value in data.items():
        notes_text += f"{key}: {value}\n"
    return notes_text.strip() if notes_text else "No notes available"

# Function to perform sentiment analysis
def analyze_sentiment(text):
    if "Error" in text or "Request failed" in text:
        return text  # Return error messages without analysis

    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(
        f"I am a learner following the \n{cc}\n roadmap. These are my daily learning notes:\n{text}\n\n"
        "Analyze my progress. Am I following the roadmap correctly, or am I diverting?"
    )
    return response.text

# Fetch and analyze sentiment for each range
notes_range1 = fetch_notes(api_urls["range1"])  # Day 1-6
sentiment_range1 = analyze_sentiment(notes_range1)

notes_range2 = fetch_notes(api_urls["range2"])  # Day 8-13
sentiment_range2 = analyze_sentiment(notes_range2)

notes_range3 = fetch_notes(api_urls["range3"])  # Day 15-20
sentiment_range3 = analyze_sentiment(notes_range3)

notes_range4 = fetch_notes(api_urls["range4"])  # Day 22-27
sentiment_range4 = analyze_sentiment(notes_range4)

# Print the sentiment results
print(f"\n📌 Sentiment Analysis (Day 1-6):\n", sentiment_range1)

