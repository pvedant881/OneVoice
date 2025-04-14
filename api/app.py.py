# api/app.py
from flask import Flask, request, render_template_string
import os
import time
import google.generativeai as genai
from utils.config import GEMINI_API_KEY, WEBSITES, DATA_FILES, MAX_PAGES, CRAWLED_DATA_FILE
from utils.data_processor import prepare_data, chunk_data, load_crawled_data
from crawlers.website_crawler import crawl_website

app = Flask(__name__)

# --- Setup Gemini API ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# --- Pre-load data (for Vercel, assume data is pre-crawled) ---
print("🔁 Loading pre-prepared data, please wait...")
start_time = time.time()

# Load local files
local_data = prepare_data(DATA_FILES)

# Load pre-crawled website data (instead of real-time crawling)
crawled_data_texts = load_crawled_data(CRAWLED_DATA_FILE)
web_data = [f"--- Pre-crawled from {item['url']} ---\n{item['text']}" for item in crawled_data_texts if 'text' in item]

combined_data = local_data + web_data

end_time = time.time()
print(f"\n✅ Data loaded in {int(end_time - start_time)} seconds.")

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = ""
    if request.method == 'POST':
        question = request.form.get('question')
        
        # Chunk data intelligently based on user's query
        relevant_chunks = chunk_data(combined_data, question)

        prompt = f"""
        You are a smart assistant with access to local business files and website data.

        A user asked: "{question}"

        Based on the data below, provide a helpful and detailed answer:

        Relevant Data:
        {''.join(relevant_chunks)}
        """
        try:
            response = model.generate_content(prompt)
            answer = response.text
        except Exception as e:
            answer = f"Error: {e}"

    return render_template_string("""
    <html>
    <head><title>Smart Business Chatbot</title></head>
    <body style="font-family: Arial; padding: 30px;">
        <h2>Ask a Question about Your Business</h2>
        <form method="post">
            <textarea name="question" rows="4" cols="80" placeholder="e.g., What are common banner sizes?">{{ request.form.question or "" }}</textarea><br><br>
            <input type="submit" value="Ask Gemini" style="padding: 10px 20px;">
        </form>
        {% if answer %}
            <hr><h3>Gemini Answer:</h3>
            <div style="white-space: pre-wrap;">{{ answer }}</div>
        {% endif %}
    </body>
    </html>
    """, answer=answer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)