import json
import re
from ai_client import generate_text, demo_message

def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    start, end = text.find("["), text.rfind("]")
    if start >= 0 and end > start:
        return text[start:end + 1]
    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start:
        return text[start:end + 1]
    return text

def _demo_quiz(topic: str):
    return {
        "title": f"Practice quiz: {topic}",
        "questions": [
            {
                "question": f"What is a useful first step when learning {topic}?",
                "options": ["Understand the basic concepts", "Skip all fundamentals", "Memorize random words", "Avoid practice"],
                "answer": 0,
                "explanation": "Start with the fundamentals, then build toward harder ideas."
            },
            {
                "question": "Which activity usually helps check understanding?",
                "options": ["Never reviewing", "Practising questions", "Ignoring mistakes", "Only reading the title"],
                "answer": 1,
                "explanation": "Practice questions help you find what you understand and what needs revision."
            },
            {
                "question": "What should you do after getting a question wrong?",
                "options": ["Give up", "Guess without checking", "Review the explanation and try again", "Skip the whole topic forever"],
                "answer": 2,
                "explanation": "Reviewing feedback helps you learn from mistakes."
            }
        ]
    }

async def generate_quiz(source: str, level: str = "Beginner") -> dict:
    prompt = f"""
Create exactly 3 multiple-choice questions for a learner at level {level}.
Use this topic or passage:
{source}

Return ONLY valid JSON with this schema:
{{
  "title": "short title",
  "questions": [
    {{
      "question": "question text",
      "options": ["option A", "option B", "option C", "option D"],
      "answer": 0,
      "explanation": "brief explanation"
    }}
  ]
}}
The answer field must be a zero-based integer from 0 to 3. Each question must have exactly four options.
"""
    result = await generate_text(prompt, "You create fair educational quizzes and return strict JSON only.")
    if not result:
        return _demo_quiz(source)
    try:
        data = json.loads(clean_json_block(result))
        if isinstance(data, list):
            data = {"title": f"Quiz: {source[:60]}", "questions": data}
        questions = data.get("questions", [])
        valid = []
        for q in questions[:3]:
            opts = q.get("options", [])
            answer = q.get("answer", 0)
            if isinstance(answer, str):
                answer = ord(answer.strip().upper()[:1]) - ord("A")
            if q.get("question") and len(opts) == 4 and isinstance(answer, int) and 0 <= answer <= 3:
                valid.append({
                    "question": str(q["question"]),
                    "options": [str(x) for x in opts],
                    "answer": answer,
                    "explanation": str(q.get("explanation", "Review the concept to understand the answer."))
                })
        if len(valid) != 3:
            raise ValueError("The model did not return exactly three valid questions.")
        return {"title": str(data.get("title", f"Quiz: {source[:60]}")), "questions": valid}
    except (ValueError, TypeError, json.JSONDecodeError):
        return _demo_quiz(source)
