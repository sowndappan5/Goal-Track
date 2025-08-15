from flask import render_template, request
import requests
import google.generativeai as genai
import markdown


GEMINI_API_KEY = 'API'
if not GEMINI_API_KEY:
    raise ValueError("Please set the GEMINI_API_KEY environment variable")
genai.configure(api_key=GEMINI_API_KEY)

def generate_roadmap_get(domain, job):
    prompt = (
        f"Create a detailed step-by-step roadmap for a beginner to become a {job} in the {domain} domain. Structure the roadmap using Roman numerals (e.g., I, II, III) and cover the following: "
         "1.Foundational skills to master first (e.g., core programming, mathematics, or domain basics).\n"
         "2.Tools and technologies critical to the field.\n"
         "3.Core concepts and techniques to learn, with practical examples where applicable.\n"
         "4.Ways to gain hands-on experience and real-world skills.\n"
         "5.Steps to build a strong portfolio showcasing expertise.\n"
         "6.Advanced knowledge areas, specializations, and strategies for contributing to the field.\n"
         "Ensure the roadmap is actionable, concise, and easy to follow without specifying time durations."
    )

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

def index1_get():
    # Retrieve domain and job from query parameters
    domain = request.args.get('domain')
    job = request.args.get('job')

    if not domain or not job:
        return "Error: Missing 'domain' or 'job' in the request", 400

    # Generate roadmap dynamically for the provided domain and job
    roadmap = generate_roadmap_get(domain, job)

    # Save the roadmap to a README.md file
    filename = "README.md"
    with open(filename, 'w') as file:
        file.write(f"# Roadmap to Become a {job} in the {domain} Domain\n\n")
        file.write(roadmap)

    # Parse the roadmap to extract timeline phases
    phases = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            # Extract Roman numeral sections (e.g., "I. Foundational Skills") or sections in bold (**Text**)
            if line.startswith("**") and line.endswith("**"):
                phases.append(line.strip("*"))  # Remove the "**"
            elif line[:2].isupper() and line[1] == ".":
                phases.append(line.split(".", 1)[1].strip())  # Extract the part after "I.", "II.", etc.

    # Create timeline data
    timeline_data = [{"phase": f"Phase {i + 1}", "title": title} for i, title in enumerate(phases)]

    # Render the timeline on the index1.html template
    return render_template('index1.html', timeline_data=timeline_data)

# Function to read markdown files
def read_markdown_file(file_path):
    """Read the contents of a markdown file."""
    with open(file_path, 'r') as file:
        return file.read()

# Function to generate a detailed roadmap using Gemini API
def generate_detailed_roadmap(file_content):
    """Generate a detailed roadmap using Gemini API."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Analyze the following roadmap and provide a comprehensive, student-friendly breakdown:

    Content to Analyze:
    {file_content}

    Please generate a structured response that includes: (Give the job and domain on top)
    1. Main Titles (Sections of the Roadmap)
    2. Topics under each Title
    3. Subtopics for each Topic
    4. Key Learning Points for each Subtopic
    5. If possible give learning platform names in the bottom of the roadmap.
    6. Dont provide 'phase' text, give like **1. Networking Fundamentals**

    example output format:
    ## I. Foundational Skills

This section focuses on the core knowledge needed before diving into penetration testing tools and techniques.

**1. Networking Fundamentals**

* **Subtopics:**
    * TCP/IP Model: Understanding how data travels across networks.
    * Subnetting: Dividing networks into smaller, manageable subnetworks.
    * IP Addressing: Assigning unique addresses to devices on a network.
    * Routing: Directing network traffic between different networks.
    * DNS: Translating domain names into IP addresses.
    * Common Network Protocols:  HTTP, HTTPS, FTP, SMTP, etc., and their vulnerabilities.

* **Key Learning Points:**  You need to grasp how networks function at a low level to understand how attacks work.  Focus on the "why" behind each concept, not just the "how".

    Use markdown formatting to make the output clear and easy to read.
    Ensure the roadmap is detailed, educational, and provides a clear learning path.
    Format should be hierarchical and easy to follow.
    """.strip()

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating roadmap: {str(e)}"

# Function to save the roadmap to a file
def save_roadmap_to_file(roadmap_content, filename='learn.md'):
    """Save roadmap content to a markdown file."""
    try:
        with open(filename, 'w') as file:
            file.write(roadmap_content)
        return roadmap_content
    except Exception as e:
        return f"Error saving file: {e}"
    
def detailed_roadmap_get():
    file_path = 'readme.md'  # The file to read
    try:
        # Read file content
        file_content = read_markdown_file(file_path)
        
        # Generate detailed roadmap
        detailed_roadmap = generate_detailed_roadmap(file_content)
        
        # Save to learn.md
        save_roadmap_to_file(detailed_roadmap)
        
        # Convert markdown to HTML
        html_content = markdown.markdown(detailed_roadmap, extensions=['fenced_code', 'tables'])
        
        # Render HTML template
        return render_template('roadmap.html', roadmap_content=html_content)
    
    except Exception as e:
        return f"An error occurred: {e}"