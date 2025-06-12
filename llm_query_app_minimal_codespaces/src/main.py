from flask import Flask, request, render_template
import requests
from utils.logger import setup_logger
from utils.helpers import get_env_var
from dotenv import load_dotenv

load_dotenv()
logger = setup_logger()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/query', methods=['POST'])
def query():
    user_query = request.form['user_query']
    logger.info(f"User Query: {user_query}")

    groq_res = "This is a placeholder Groq response."
    gemini_res = "This is a placeholder Gemini response."

    logger.info(f"Groq Response: {groq_res}")
    logger.info(f"Gemini Response: {gemini_res}")

    return render_template("index.html", groq_response=groq_res, gemini_response=gemini_res)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
