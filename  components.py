import streamlit as st
import requests
import json

# --- CONFIG ---
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_groq_headers():
    try:
        if 'GROQ_API_KEY' not in st.secrets:
            st.error("❌ Groq API key not found. Add GROQ_API_KEY to secrets.toml")
            return None
        return {
            "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}",
            "Content-Type": "application/json"
        }
    except Exception as e:
        st.error(f"❌ Error accessing Groq API key: {str(e)}")
        return None

def groq_query(prompt, model="llama3-8b-8192"):
    """Query Groq API"""
    headers = get_groq_headers()
    if not headers:
        return "❌ API headers not configured"
    
    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": model,
        "temperature": 0.1,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            return f"❌ Error: {response.status_code} - {response.text}"
            
    except requests.exceptions.Timeout:
        return "❌ Request timed out. Please try again."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- Functional Components ---
def explain_code(code, language="python"):
    if not code or not code.strip():
        st.error("❌ Please provide some code to explain!")
        return
        
    with st.container():
        st.markdown("""<div style='background-color:#f9f9f9;padding:15px;border-radius:10px;border-left:4px solid #007acc;'>""", unsafe_allow_html=True)
        st.subheader("📖 Code Explanation")
        
        with st.spinner("Analyzing your code..."):
            prompt = f"""Explain this {language} code step by step in simple terms:

```{language}
{code}
```

Break down what each part does and explain the overall purpose. Keep it beginner-friendly."""
            
            result = groq_query(prompt)
            st.write(result)
        st.markdown("""</div>""", unsafe_allow_html=True)

def debug_code(code):
    if not code or not code.strip():
        st.error("❌ Please provide some code to debug!")
        return
        
    with st.container():
        st.markdown("""<div style='background-color:#fff3cd;padding:15px;border-radius:10px;border-left:4px solid #ffc107;'>""", unsafe_allow_html=True)
        st.subheader("🐛 Debug Analysis")
        
        with st.spinner("Debugging your code..."):
            prompt = f"""Analyze this code for bugs, errors, and improvements:

```
{code}
```

Identify:
1. Syntax errors
2. Logic issues
3. Best practice violations
4. Suggested improvements"""
            
            result = groq_query(prompt)
            st.write(result)
        st.markdown("""</div>""", unsafe_allow_html=True)

def show_lessons(language):
    with st.container():
        st.markdown("""<div style='background-color:#e7f3fe;padding:15px;border-radius:10px;border-left:4px solid #0066cc;'>""", unsafe_allow_html=True)
        st.subheader(f"{language.capitalize()} Learning Resources")
        
        with st.spinner(f"Loading {language} lessons..."):
            prompt = f"""Create a beginner-friendly {language} programming tutorial covering:

1. Basic syntax and concepts
2. Common use cases
3. Simple example with explanation
4. Next steps for learning"""
            
            result = groq_query(prompt)
            st.write(result)
        st.markdown("""</div>""", unsafe_allow_html=True)

def show_quiz(language):
    with st.container():
        st.markdown("""<div style='background-color:#f0fdf4;padding:15px;border-radius:10px;border-left:4px solid #22c55e;'>""", unsafe_allow_html=True)
        st.subheader("Mini Quiz")
        
        with st.spinner("Generating quiz..."):
            prompt = f"""Create a {language} programming quiz question for beginners with multiple choice answers and explanation."""
            
            result = groq_query(prompt)
            st.write(result)
        st.markdown("""</div>""", unsafe_allow_html=True)

def show_career_advice(path):
    with st.container():
        st.markdown("""<div style='background-color:#fef6f6;padding:15px;border-radius:10px;border-left:4px solid #ef4444;'>""", unsafe_allow_html=True)
        st.subheader("Career Guidance")
        
        with st.spinner("Generating career advice..."):
            prompt = f"""Provide practical career advice for becoming a {path} developer including skills, learning path, and job search tips."""
            
            result = groq_query(prompt)
            st.write(result)
        st.markdown("""</div>""", unsafe_allow_html=True)