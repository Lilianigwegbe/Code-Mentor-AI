import streamlit as st
import requests
import json

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Code Mentor AI", 
    layout="centered",
    page_icon="💡",
    initial_sidebar_state="expanded"
)

# --- GROQ API CONFIGURATION ---
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_groq_headers():
    """Get Groq API headers with error handling"""
    try:
        if 'GROQ_API_KEY' not in st.secrets:
            st.error("❌ Groq API key not found. Please add GROQ_API_KEY to your secrets.toml file.")
            st.info("Get your free API key at: https://console.groq.com/keys")
            return None
        return {
            "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}",
            "Content-Type": "application/json"
        }
    except Exception as e:
        st.error(f"❌ Error accessing Groq API key: {str(e)}")
        return None

def groq_query(prompt, model="llama3-8b-8192", max_tokens=1000):
    """Query Groq API with improved error handling"""
    headers = get_groq_headers()
    if not headers:
        return "❌ API configuration error"
    
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful programming mentor. Provide clear, accurate, and educational responses about code, programming concepts, and career advice."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "model": model,
        "temperature": 0.1,
        "max_tokens": max_tokens,
        "top_p": 1,
        "stream": False
    }
    
    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        elif response.status_code == 429:
            return "❌ Rate limit exceeded. Please wait a moment and try again."
        elif response.status_code == 401:
            return "❌ Invalid API key. Please check your GROQ_API_KEY in secrets.toml"
        else:
            return f"❌ API Error: {response.status_code} - {response.text[:200]}"
            
    except requests.exceptions.Timeout:
        return "❌ Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return "❌ Connection error. Please check your internet connection."
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

# --- COMPONENT FUNCTIONS ---
def explain_code(code, language="python"):
    """Explain code with input validation"""
    if not code or not code.strip():
        st.error("❌ Please provide some code to explain!")
        return
        
    with st.container():
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                    padding: 20px; border-radius: 15px; border-left: 5px solid #007acc; 
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: 10px 0;'>
        """, unsafe_allow_html=True)
        
        st.subheader("📖 Code Explanation")
        
        # Show the code being analyzed
        st.code(code, language=language)
        
        with st.spinner("🔍 Analyzing your code..."):
            prompt = f"""Explain this {language} code step by step in simple terms:

```{language}
{code}
```

Please provide:
1. **Overall Purpose**: What does this code do?
2. **Step-by-Step Breakdown**: Explain each significant part
3. **Key Concepts**: Highlight important programming concepts used
4. **Potential Use Cases**: Where might this code be useful?

Keep the explanation clear and beginner-friendly."""
            
            result = groq_query(prompt)
            st.markdown(result)
            
        st.markdown("</div>", unsafe_allow_html=True)

def debug_code(code):
    """Debug code with input validation"""
    if not code or not code.strip():
        st.error("❌ Please provide some code to debug!")
        return
        
    with st.container():
        st.markdown("""
        <div style='background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); 
                    padding: 20px; border-radius: 15px; border-left: 5px solid #ffc107; 
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: 10px 0;'>
        """, unsafe_allow_html=True)
        
        st.subheader("🐛 Debug Analysis")
        
        # Show the code being debugged
        st.code(code)
        
        with st.spinner("🔧 Debugging your code..."):
            prompt = f"""Analyze this code for bugs, errors, and improvements:

```
{code}
```

Please provide:
1. **Syntax Errors**: Any syntax issues that would prevent the code from running
2. **Logic Issues**: Problems with the code logic or flow
3. **Best Practice Violations**: Areas where the code could follow better practices
4. **Security Concerns**: Any potential security issues
5. **Performance Improvements**: Ways to make the code more efficient
6. **Suggested Fixes**: Specific recommendations with example corrections

Be thorough but constructive in your analysis."""
            
            result = groq_query(prompt)
            st.markdown(result)
            
        st.markdown("</div>", unsafe_allow_html=True)

def show_lessons(language):
    """Show programming lessons"""
    with st.container():
        st.markdown("""
        <div style='background: linear-gradient(135deg, #e7f3fe 0%, #a8e6cf 100%); 
                    padding: 20px; border-radius: 15px; border-left: 5px solid #0066cc; 
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: 10px 0;'>
        """, unsafe_allow_html=True)
        
        st.subheader(f"📚 {language.capitalize()} Learning Resources")
        
        with st.spinner(f"📖 Loading {language} lessons..."):
            prompt = f"""Create a comprehensive beginner-friendly {language} programming tutorial:

Please cover:
1. **Introduction**: Brief overview of {language} and its uses
2. **Basic Syntax**: Core syntax elements and rules
3. **Key Concepts**: Important programming concepts in {language}
4. **Practical Example**: A simple, complete example with explanation
5. **Common Mistakes**: What beginners should avoid
6. **Next Steps**: Recommended learning path and resources

Make it educational, practical, and encouraging for beginners."""
            
            result = groq_query(prompt, max_tokens=1500)
            st.markdown(result)
            
        st.markdown("</div>", unsafe_allow_html=True)

def show_quiz(language):
    """Generate programming quiz"""
    with st.container():
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); 
                    padding: 20px; border-radius: 15px; border-left: 5px solid #22c55e; 
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: 10px 0;'>
        """, unsafe_allow_html=True)
        
        st.subheader("🧠 Mini Quiz")
        
        with st.spinner("🎯 Generating quiz..."):
            prompt = f"""Create a {language} programming quiz question for beginners:

Format your response as:
**Question:** [Clear, specific question about {language}]

**Options:**
A) [Option 1]
B) [Option 2] 
C) [Option 3]
D) [Option 4]

**Answer:** [Correct letter] 

**Explanation:** [Why this answer is correct and why others are wrong]

**Learning Tip:** [A helpful tip related to this concept]

Make it educational, practical, and test real programming knowledge that beginners should learn."""
            
            result = groq_query(prompt)
            st.markdown(result)
            
        st.markdown("</div>", unsafe_allow_html=True)

def show_career_advice(path):
    """Provide career guidance"""
    with st.container():
        st.markdown("""
        <div style='background: linear-gradient(135deg, #fef6f6 0%, #fecaca 100%); 
                    padding: 20px; border-radius: 15px; border-left: 5px solid #ef4444; 
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: 10px 0;'>
        """, unsafe_allow_html=True)
        
        st.subheader("💼 Career Guidance")
        
        with st.spinner("💡 Generating career advice..."):
            prompt = f"""Provide comprehensive career advice for becoming a successful {path} developer:

Please include:
1. **Required Skills**: Essential technical skills and technologies
2. **Learning Roadmap**: Step-by-step learning path with timeline
3. **Portfolio Projects**: 5-7 project ideas to build a strong portfolio
4. **Job Search Strategy**: How to find and apply for jobs
5. **Interview Preparation**: Common questions and how to prepare
6. **Salary Expectations**: General salary ranges for different experience levels
7. **Career Growth**: Advancement opportunities and specializations
8. **Industry Insights**: Current trends and future outlook

Make the advice current, practical, and actionable for someone starting their career."""
            
            result = groq_query(prompt, max_tokens=1500)
            st.markdown(result)
            
        st.markdown("</div>", unsafe_allow_html=True)

# --- MAIN APP ---
def main():
    # Header
    st.title("💡 Code Mentor AI")
    st.markdown("*Your AI-powered programming assistant*")
    
    # Sidebar
    with st.sidebar:
        st.header("🛠️ Options")
        
        # Task selection
        task = st.selectbox(
            "Choose a task", 
            ["Explain Code", "Debug Code", "Show Lessons", "Mini Quiz", "Career Advice"],
            help="Select what you'd like help with"
        )
        
        # Language selection
        language = st.selectbox(
            "Programming Language", 
            ["python", "javascript", "java", "c++", "html", "css", "sql", "go", "rust"],
            help="Choose the programming language"
        )
        
        # Career path selection
        career_path = st.selectbox(
            "Career Path", 
            ["frontend", "backend", "fullstack", "data-science", "machine-learning", "devops", "mobile"],
            help="Select your target career path"
        )
        
        st.markdown("---")
        st.markdown("### 🚀 Tips:")
        st.markdown("• Paste complete, runnable code for best explanations")
        st.markdown("• Try different languages to explore new concepts")
        st.markdown("• Use career advice to plan your learning journey")
    
    # Main content area
    if task == "Explain Code":
        st.markdown("### 📝 Code Input")
        user_code = st.text_area(
            "Paste your code here", 
            height=200,
            placeholder=f"Enter your {language} code here...",
            help="Paste the code you want explained"
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔍 Explain Code", type="primary", use_container_width=True):
                if user_code.strip():
                    explain_code(user_code, language)
                else:
                    st.warning("⚠️ Please enter some code to explain!")

    elif task == "Debug Code":
        st.markdown("### 🐛 Code to Debug")
        user_code = st.text_area(
            "Paste your code here", 
            height=200,
            placeholder="Enter code that might have issues...",
            help="Paste the code you want debugged"
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔧 Debug Code", type="primary", use_container_width=True):
                if user_code.strip():
                    debug_code(user_code)
                else:
                    st.warning("⚠️ Please enter some code to debug!")

    elif task == "Show Lessons":
        st.markdown(f"### 📚 Learn {language.capitalize()}")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(f"📖 Show {language.capitalize()} Lessons", type="primary", use_container_width=True):
                show_lessons(language)

    elif task == "Mini Quiz":
        st.markdown(f"### 🧠 Test Your {language.capitalize()} Knowledge")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(f"🎯 Generate {language.capitalize()} Quiz", type="primary", use_container_width=True):
                show_quiz(language)

    elif task == "Career Advice":
        st.markdown(f"### 💼 {career_path.replace('-', ' ').title()} Career Path")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(f"💡 Get {career_path.replace('-', ' ').title()} Advice", type="primary", use_container_width=True):
                show_career_advice(career_path)

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Built with Streamlit • Powered by Groq API"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()