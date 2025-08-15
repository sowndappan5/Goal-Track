import requests

# Your Gemini API key
GEMINI_API_KEY = 'AIzaSyB335UzzSBBxHj94igOEAThkn_G_uFP9UY'  # Replace with your actual API key

def generate_duration_from_gemini(roadmap_content):
    """Send a request to Gemini API to get duration for the roadmap."""
    prompt = f"Based on the following roadmap, provide estimated durations and what are the things we learn for each subtopics for first three sections:\n\n{roadmap_content}"

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}", headers=headers, json=payload)

    if response.status_code == 200:
        response_data = response.json()
        if 'candidates' in response_data:
            return response_data['candidates'][0]['content']['parts'][0]['text']
        return "No generated content found in the response."
    return f"Error: {response.status_code} - {response.text}"

def main():
    # Read the learn.md file
    try:
        with open('learn.md', 'r') as file:
            roadmap_content = file.read()
        
        # Get duration from Gemini API
        duration_info = generate_duration_from_gemini(roadmap_content)
        
        # Print the duration information to the terminal
        print("Estimated Duration for Roadmap:")
        print(duration_info)
    
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

if __name__ == '__main__':
    main()
