from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app, origins=["https://devdual.com"])
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

@app.route("/", methods=["GET", "POST"])
def home():
    questions = []
    if request.method == "POST":
        text = request.form.get("text", "")
        questions = generate_questions(text)
    return render_template("index.html", questions=questions)

@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.get_json()
    text = data.get("text", "")
    questions = generate_questions(text)
    return jsonify({"questions": questions})

import os
import requests

def generate_questions(text):
    api_key = os.getenv("COHERE_API_KEY")  # Environment variable
    if not api_key:
        return ["Cohere API key not set."]
    
    url = "https://api.cohere.ai/v1/generate"
    prompt = f"Generate 5 quiz questions (multiple choice or fill-in-the-blanks) from the following text:\n\n{text}\n\n"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "command-r",
        "prompt": prompt,
        "max_tokens": 300,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        if "generations" in data:
            content = data["generations"][0].get("text", "")
            return content.strip().split("\n") if content else ["No content generated."]
        else:
            return [f"Error: {data.get('message', 'Unexpected response')}"]
    except Exception as e:
        return [f"Exception: {str(e)}"]
except Exception as e:
    return [f"Sorry! An error occurred while generating questions. ({str(e)})"]
