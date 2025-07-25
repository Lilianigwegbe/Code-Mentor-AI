# components.py
import streamlit as st
from data import (
    CODE_EXPLANATIONS,
    DEBUG_PATTERNS,
    MINI_LESSONS,
    QUIZ_QUESTIONS,
    CAREER_GUIDANCE,
)
import re

# --- Code Explanation ---
def explain_code(code, language="python"):
    st.subheader("Code Explanation")
    explanations = []
    for key, value in CODE_EXPLANATIONS.get(language, {}).items():
        pattern = value["pattern"]
        matches = re.findall(pattern, code)
        for match in matches:
            explanations.append(value["explanation"].format(match))
    if explanations:
        for exp in explanations:
            st.markdown(f"✅ {exp}")
    else:
        st.warning("No explanation found.")

# --- Debugging Help ---
def debug_code(code):
    st.subheader("Debugging Assistant")
    for key, value in DEBUG_PATTERNS.items():
        if re.search(value["pattern"], code):
            st.markdown(f"⚠️ **{key}**: {value['solution']}")
            return
    st.success("No known issues detected.")

# --- Mini Lessons ---
def show_lessons(language="python"):
    st.subheader(f"Mini Lessons - {language.title()}")
    lessons = MINI_LESSONS.get(language, [])
    for lesson in lessons:
        st.markdown(f"### {lesson['title']}")
        st.write(lesson["content"])

# --- Quiz ---
def show_quiz(language="python"):
    st.subheader(f"{language.title()} Quiz")
    questions = QUIZ_QUESTIONS.get(language, [])
    for i, q in enumerate(questions):
        st.markdown(f"**Q{i+1}. {q['q']}**")
        choice = st.radio("Choose:", q["options"], key=f"q{i}")
        if choice == q["options"][q["answer"]]:
            st.success("Correct!")
        else:
            st.error("Try again.")

# --- Career Advice ---
def show_career_advice(path="frontend"):
    st.subheader(f"Career Guidance - {path.title()}")
    advice = CAREER_GUIDANCE.get(path)
    if advice:
        st.markdown(f"**Skills Needed:** {', '.join(advice['skills'])}")
        st.markdown(f"💡 {advice['advice']}")
    else:
        st.warning("Path not found.")
