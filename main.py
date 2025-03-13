import json
import requests
from flask import Flask, request, jsonify

# Load FAQ data
with open("D:\repositories\instructLLM\faq_data.json", "r") as file:
    faq_data = json.load(file)

# OpenAI API Key (Replace with your actual key)
openai_api_key = " **** "

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_question = data.get("question", "").strip()

    # Check if the question matches the FAQ database
    answer = faq_data.get(user_question)
    
    if answer:
        return jsonify({"response": answer})

    # If no match, use OpenAI for a response
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openai_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a helpful FAQ chatbot. Answer briefly and clearly."},
                    {"role": "user", "content": user_question}
                ]
            }
        )
        response_data = response.json()
        return jsonify({"response": response_data['choices'][0]['message']['content']})
    except Exception as e:
        return jsonify({"response": "Error: Unable to get response from OpenAI."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

# To run in production, use a WSGI server like Waitress, run the following command in the terminal:
# waitress-serve --port=5000 main:app