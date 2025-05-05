from dotenv import load_dotenv
load_dotenv()  # Load all environment variables

import streamlit as st
import os
import google.generativeai as genai

# Get API key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key not found. Please set GOOGLE_API_KEY in your .env file.")
    st.stop()

# Configure API key for generative AI
genai.configure(api_key=api_key)

# Load Gemini 1.5 Pro latest model
try:
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
    chat = model.start_chat(history=[])
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.stop()

# Function to get response from Gemini
def get_gemini_response(question):
    try:
        response = chat.send_message(question)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("🤖 Gemini LLM Talk Bot")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input box and submit button
input_text = st.text_input("Ask something:", key="input")
submit = st.button("Ask")

# Handle submit
if submit and input_text:
    answer = get_gemini_response(input_text)
    st.session_state['chat_history'].append(("You", input_text))
    st.session_state['chat_history'].append(("Talk Bot", answer))

# Display chat history
st.subheader("💬 Chat History")
for role, text in st.session_state['chat_history']:
    st.markdown(f"**{role}:** {text}")
