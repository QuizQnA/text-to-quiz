# Text to Quiz Generator (Flask + OpenAI API)

This app generates quiz questions from input text using OpenAI's GPT model.

## How to Deploy on Render

1. Push this code to a GitHub repository.
2. Go to https://render.com and create a new Web Service.
3. Use the following settings:

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Environment Variable**: `OPENAI_API_KEY=your-openai-api-key`

4. Deploy and visit the URL Render provides.