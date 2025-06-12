from flask import Flask, request, render_template
import requests
from utils.logger import setup_logger
from utils.helpers import get_env_var
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
logger = setup_logger()

# Fix: tell Flask where to find the templates directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/query', methods=['POST'])
def query():
    try:
        user_query = request.form['user_query']
        logger.info(f"User Query: {user_query}")

        # Get API keys from .env
        gemini_api_key = get_env_var("GEMINI_API_KEY")
        groq_api_key = get_env_var("GROQ_API_KEY")

        # === Gemini Call ===
        import time 
        import google.generativeai as genai
        genai.configure(api_key=gemini_api_key)

        try:
            start_time = time.time()
            model = genai.GenerativeModel("gemini-1.5-flash-latest")
            gemini_response = model.generate_content(user_query)
            duration = time.time() - start_time
            gemini_text = gemini_response.text
            logger.info(f"Gemini Response Time: {duration:.2f} sec")
        except Exception as e:
            logger.error(f"Gemini Error: {e}")
            gemini_text = f"Gemini failed to respond. Error: {e}"

        # === Groq Call ===
        import requests
        try:
            groq_payload = {
                "model": "llama3-70b-8192",
                "messages": [{"role": "user", "content": user_query}],
                "temperature": 0.7
            }
            headers = {
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            }
            groq_response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=groq_payload
            )
            groq_text = groq_response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Groq Error: {e}")
            groq_text = "Groq failed to respond."

        # === Return to Template ===
        logger.info(f"Gemini: {gemini_text}")
        logger.info(f"Groq: {groq_text}")

        return render_template("index.html", gemini_response=gemini_text, groq_response=groq_text)

    except Exception as e:
        logger.error(f"Internal Server Error: {e}")
        return "500 Internal Server Error", 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

