import sys
import google.generativeai as genai

# Configure Gemini API key
GEMINI_API_KEY = "AIzaSyB335UzzSBBxHj94igOEAThkn_G_uFP9UY"
genai.configure(api_key=GEMINI_API_KEY)


# Validate user input
if len(sys.argv) < 1:
    print("Usage: python task.py <week_number>")
    sys.exit(1)  # Exit if no week number is provided

month_input = 1  # Get week number from user input

# Read the roadmap content from learn.md
try:
    with open("learn.md", "r") as file:
        learn_md_content = file.read()
except FileNotFoundError:
    print("Error: 'learn.md' file not found!")
    sys.exit(1)

# Construct the prompt
prompt = f"""
Based on the roadmap found in the learn_md_content , generate a structured 30-day task plan for month {month_input}. Give the full 30 days detailed plan and dont't miss a single day. The last day of each week should be blank.
The output format must EXACTLY match the syntax and structure of `task.md`. Always the day 7, day 14 , day 21, day 28, day 30 should be blank. Prefer one learning academy if available.Must give five task for each day. Each task should be informative and precise manner.

## Format Example (task.md):
***I. Foundational Skills***
**1. Mathematics for Blockchain**

### Day 1: Introduction to Blockchain & Cryptography
## Topics: 
- What is blockchain? Why is it important?  
- Basics of cryptography in digital currencies.  

🎯 Tasks:
✅ Watch a video on how blockchain works.  
✅ Read a short article on cryptography in blockchain (10 min).  
✅ Write down 3 key points you learned (5 min).  

---

### Day 2: Understanding Hashing (SHA-256)
## Topics:
- What is hashing? How does SHA-256 work in Bitcoin?  

🎯 Tasks:  
✅ Watch a video on SHA-256.  
✅ Read a simple example of how hashing is used in blockchain (10 min).  
✅ Try an online SHA-256 hash generator (5 min).  

---

### Day 3: Basics of Digital Signatures  
## Topics:
- What are digital signatures? Why are they important?  
- Introduction to Public and Private Keys.  

🎯 Tasks:  
✅ Read a simple explanation of digital signatures (10 min).  
✅ Watch a short video on public-private keys.  
✅ Write down 2 real-world use cases of digital signatures (5 min).  

---

### Day 4: Introduction to Data Structures (Arrays & Lists)  
## Topics:  
- What are arrays and linked lists?  
- Where are they used in blockchain?  
 
🎯 Tasks:  
✅ Watch a 5-minute video on arrays.  
✅ Try a simple Python example of an array (10 min).  
✅ Solve 1 small array-related problem (10 min).  

---

### Day 5: Basics of Networking (HTTP & HTTPS)
## Topics:
- What is HTTP and HTTPS? Why is HTTPS more secure?  

🎯 Tasks:  
✅ Read a short article on how HTTPS works (10 min).  
✅ Watch a 5-minute video explaining HTTP vs HTTPS.  
✅ Write 2 key differences between HTTP and HTTPS (5 min).  

---

### Day 6: Real-World Use Cases of Blockchain  
## Topics:  
- How is blockchain used in payments?  
- Examples: Bitcoin, Ethereum, CBDCs.  

🎯 Tasks:  
✅ Watch a 5-minute video on Bitcoin.  
✅ Read about Ethereum and smart contracts (10 min).  
✅ Write 2 industries where blockchain is transforming payments (5 min).

## Roadmap Content:
{learn_md_content}
"""

# Send request to Gemini API
model = genai.GenerativeModel("gemini-1.5-flash")  # Using the latest stable version
def generate():
    response = model.generate_content(prompt)

# Save output to task.md
    with open("task.md", "w", encoding="utf-8") as task_file:
        task_file.write(response.text)


    print(f"✅ Daily task content for Month {month_input} has been generated in 'task.md'")
