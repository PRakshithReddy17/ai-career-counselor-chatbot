from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from rag import search

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str


# 🔥 OPENROUTER AI FUNCTION
def query_ai(prompt):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openrouter/auto",
                "messages": [
                    {"role": "system", "content": "You are a helpful career counselor."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 300
            },
            timeout=30
        )

        result = response.json()
        print("AI RESPONSE:", result)

        # ✅ Success
        if "choices" in result:
            return result["choices"][0]["message"]["content"]

        # ❌ Error case
        if "error" in result:
            return f"API Error: {result['error'].get('message', 'Unknown error')}"

        return "Unexpected response from AI."

    except Exception as e:
        print("ERROR:", e)
        return "Error connecting to AI service."


# 🔥 MAIN LOGIC
def get_response(user_input):
    try:
        context = search(user_input)

        prompt = f"""
You are an AI career counselor.

Give short, clear, and helpful career advice.

Career Data:
{context}

User Question:
{user_input}
"""

        return query_ai(prompt)

    except Exception as e:
        print("MAIN ERROR:", e)
        return "Something went wrong."


# 🔥 API ROUTE
@app.post("/chat")
def chat(request: ChatRequest):
    return {"reply": get_response(request.message)}