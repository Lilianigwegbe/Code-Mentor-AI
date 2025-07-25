import json
import os

DATA_DIR = "data"

def load_json(filename):
    with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
        return json.load(f)

CODE_EXPLANATIONS = load_json("code_explanations.json")
DEBUG_PATTERNS = load_json("debug_patterns.json")
MINI_LESSONS = load_json("mini_lessons.json")
QUIZ_QUESTIONS = load_json("quiz_questions.json")
CAREER_GUIDANCE = load_json("career_guidance.json")
