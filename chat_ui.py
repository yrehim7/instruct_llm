import streamlit as st
import requests

# Streamlit UI
st.title("🤖 FAQ Chatbot")
st.write("Ask a question and get an instant response!")

# Input field for user query
user_input = st.text_input("Your question:")

# Send request when the button is clicked
if st.button("Get Answer"):
    if user_input.strip():
        response = requests.post(
            "http://127.0.0.1:5000/chat",
            json={"question": user_input}
        )
        if response.status_code == 200:
            st.write("**Answer:**", response.json().get("response", "No response available."))
        else:
            st.write("❌ Error:", response.text)
    else:
        st.warning("Please enter a question before submitting.")
