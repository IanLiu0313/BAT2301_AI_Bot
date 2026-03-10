# ==============================================
# Course Agent for BAT2301
# Framework developed and implemented by Ian Liu in 2026
# Ian Liu, faculty at Trinity University, SATX
# All rights reserved.
# Do not copy, use, or distribute this code 
# without express written permission.
# ===============================================

import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="Course AI Agent", page_icon="🎓")

# --- API KEY SETUP ---
# Safely pulls the key from .streamlit/secrets.toml (local) OR Streamlit Cloud Secrets (web)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("API Key not found! Please check your secrets.toml file.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- LOAD DATA ---
@st.cache_data
def load_context():
    try:
        with open("course_data.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

course_context = load_context()

# --- INTERFACE ---
st.title("🎓 BAT/ECON2301 AI Assistant")
st.markdown("Ask any question about the **syllabus**, **schedule**,  **course content**, and/or **exam prep guides**.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle Chat Input
if prompt := st.chat_input("Ex: When is the midterm?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not course_context:
        st.error("⚠️ System Error: 'course_data.txt' not found. Please run prep_data.py.")
    else:
        try:
            full_prompt = f"""
            You are a polite and helpful Teaching Assistant.
            Answer the student's question specifically using the COURSE CONTEXT below.
            If the answer is not in the text, state that you do not know and advise them to email the professor.
            
            COURSE CONTEXT:
            {course_context}
            
            STUDENT QUESTION:
            {prompt}
            """
            
            with st.spinner("Wow, that's good question. I'm thinking at the speed of a sloth swimming through peanut butter. Please stand by."):
                response = model.generate_content(full_prompt)
                
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            with st.chat_message("assistant"):
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")