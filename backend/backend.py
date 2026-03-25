import ollama
from rag import search
import re


def is_english(text):
    # Simple check: if text contains mostly English characters
    return bool(re.match(r'^[A-Za-z0-9\s.,!?]+$', text))


def get_response(user_input):
    try:
        context = search(user_input)

        # Detect if input is English
        english_input = is_english(user_input)

        if english_input:
            language_instruction = "Reply ONLY in English."
        else:
            language_instruction = "Reply ONLY in the same language as the user."

        prompt = f"""
You are an AI career counselor for rural students.

STRICT RULES:
- {language_instruction}
- DO NOT switch language
- DO NOT explain language
- Keep answer short (4-5 lines)
- Use simple and practical advice
- Include career, exams, and colleges if available

Career Data:
{context}

User Question:
{user_input}
"""

        response = ollama.chat(
            model="phi3",
            messages=[{"role": "user", "content": prompt}]
        )

        return response["message"]["content"]

    except Exception as e:
        print("ERROR:", str(e))
        return "Something went wrong. Please try again."