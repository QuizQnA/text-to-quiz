from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body)
        data = response.json()
        content = data['choices'][0]['message']['content']
        return content.strip().split('\n') if content else []
    except Exception as e:
        return [f"Error: {str(e)}"]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)