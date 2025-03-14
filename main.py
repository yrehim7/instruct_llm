import json
import requests
from flask import Flask, request, jsonify

# Load FAQ data
with open("faq_data.json", "r") as file:
    faq_data = json.load(file)

# OpenAI API Key (Replace with your actual key)
openai_api_key = "----"

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    if request.method != "POST":
        return jsonify({"response": "Error: Method not allowed."}), 405

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
        print("OpenAI API Response:", response_data)  # Debug statement

        if "choices" in response_data:
            return jsonify({"response": response_data['choices'][0]['message']['content']})
        else:
            return jsonify({"response": f"Error: Unexpected response from OpenAI. {response_data}"}), 500
    except Exception as e:
        return jsonify({"response": f"Error: Unable to get response from OpenAI. {str(e)}"}), 500

if __name__ == "__main__":
    # Run the Flask app # To run in production, use a WSGI server like Waitress, run the following command in the terminal:
    app.debug = True
    app.run(host='0.0.0.0', port=5000)