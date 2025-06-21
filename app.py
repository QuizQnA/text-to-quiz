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

def generate_questions(text):
    prompt = f"Generate 5 quiz questions (MCQs or fill in the blanks) based on this text:\n{text}"
    headers = {
        "Authorization": f"Bearer {os.getenv('COHERE_API_KEY')}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "command-r",  # Or "command", depending on your account
        "prompt": prompt,
        "max_tokens": 300,
        "temperature": 0.7,
    }
    try:
        response = requests.post("https://api.cohere.ai/v1/generate", headers=headers, json=body)
        data = response.json()
        content = data.get("generations", [{}])[0].get("text", "")
        return content.strip().split('\n') if content else ["No content returned."]
    except Exception as e:
        return [f"Error: {str(e)}"]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
