import json
import requests
from flask import Flask, request, jsonify

# Load FAQ data
with open("faq_data.json", "r") as file:
    faq_data = json.load(file)

# Claude API Key (Replace with your actual key)
# Replace with your Claude.ai API key
claude_api_key = "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"

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
   # If no match, use Claude.ai for a response
    try:
        response = requests.post(
            "https://api.claude.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {claude_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "messages": [
                    {"role": "system", "content": "You are a helpful FAQ chatbot. Answer briefly and clearly."},
                    {"role": "user", "content": user_question}
                ]
            }
        )
        response_data = response.json()
        return jsonify({"response": response_data['choices'][0]['message']['content']})
    except Exception as e:
        return jsonify({"response": "Error: Unable to get response from Claude.ai."})

if __name__ == "__main__":
    app.run(debug=True)
