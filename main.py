import json
from flask import Flask, request, jsonify
import logging
from langchain.chat_models import ChatAnthropic  # Updated to use Anthropic's model
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings  # Keeping OpenAI embeddings unless switching to Claude-compatible embeddings

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load FAQ data
logging.debug("Loading FAQ data")
with open("faq_data.json", "r") as file:
    faq_data = json.load(file)
logging.debug("FAQ data loaded")

claude_api_key = "-------"

app = Flask(__name__)

# Initialize LangChain components
logging.debug("Initializing LangChain components")
llm = ChatAnthropic(anthropic_api_key=claude_api_key, model="claude-2")  # Updated to use Claude
prompt_template = PromptTemplate(
    input_variables=["question"],
    template="You are a helpful FAQ chatbot. Answer briefly and clearly.\n\nUser: {question}\nChatbot:"
)
llm_chain = LLMChain(llm=llm, prompt=prompt_template)
logging.debug("LangChain components initialized")

# Initialize vector store
logging.debug("Initializing vector store")
embeddings = OpenAIEmbeddings(openai_api_key=claude_api_key)  # Keeping OpenAI embeddings for now
faq_texts = list(faq_data.keys())
faq_vectors = FAISS.from_texts(faq_texts, embeddings)
logging.debug("Vector store initialized")

@app.route("/chat", methods=["POST"])
def chat():
    logging.debug("Received a request at /chat endpoint")
    if request.method != "POST":
        logging.error("Method not allowed")
        return jsonify({"response": "Error: Method not allowed."}), 405

    try:
        data = request.get_json()
        logging.debug(f"Request data: {data}")
        user_question = data.get("question", "").strip()
        logging.debug(f"User question: {user_question}")

        # Check if the question matches the FAQ database using vector search
        logging.debug("Searching for the most relevant FAQ answer")
        search_results = faq_vectors.similarity_search(user_question, k=1)
        if search_results:
            answer = faq_data.get(search_results[0].text)
            logging.debug(f"Found answer in FAQ: {answer}")
            return jsonify({"response": answer})

        # If no match, use LangChain for a response
        logging.debug("No match in FAQ, using LangChain for response")
        response = llm_chain.run(user_question)
        logging.debug(f"Response from LangChain: {response}")
        return jsonify({"response": response})
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"response": f"Error: Unable to process request. {str(e)}"}), 500

if __name__ == "__main__":
    logging.info("Starting Flask app")
    app.run(host='0.0.0.0', port=5000, threaded=True)