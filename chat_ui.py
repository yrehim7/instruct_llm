import streamlit as st
import requests

# Set up the Streamlit app
st.title("💬 FAQ Chatbot")
st.write("Ask a question and continue the conversation!")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input field
user_input = st.chat_input("Type your question here...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Send request to Flask API
    response = requests.post(
        "http://127.0.0.1:5000/chat",
        json={"question": user_input}
    )

    # Get response from chatbot
    if response.status_code == 200:
        bot_response = response.json().get("response", "No response available.")
    else:
        bot_response = "❌ Error: Could not get a response."

    # Add chatbot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # Refresh the page to show the updated conversation
    st.rerun()
