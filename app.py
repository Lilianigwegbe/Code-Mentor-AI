# app.py
import streamlit as st
from components import (
    explain_code,
    debug_code,
    show_lessons,
    show_quiz,
    show_career_advice
)

# --- Page Setup ---
st.set_page_config(page_title="AI Code Mentor", layout="wide")
st.title("🤖 AI Code Mentor")

# --- Sidebar Navigation ---
menu = st.sidebar.selectbox("Choose a Feature", [
    "Code Explanation",
    "Debug My Code",
    "Mini Lessons",
    "Quiz Me",
    "Career Guidance"
])

# --- Feature Routing ---
if menu == "Code Explanation":
    lang = st.selectbox("Language", ["python", "javascript"])
    code_input = st.text_area("Paste your code here:")
    if st.button("Explain"):
        explain_code(code_input, language=lang)

elif menu == "Debug My Code":
    code_input = st.text_area("Paste code to debug:")
    if st.button("Check for Bugs"):
        debug_code(code_input)

elif menu == "Mini Lessons":
    lang = st.selectbox("Select Language", ["python", "javascript"])
    show_lessons(language=lang)

elif menu == "Quiz Me":
    lang = st.selectbox("Choose Language", ["python", "javascript"])
    show_quiz(language=lang)

elif menu == "Career Guidance":
    path = st.selectbox("Choose your path", ["frontend", "backend"])
    show_career_advice(path=path)
