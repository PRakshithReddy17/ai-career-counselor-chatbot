from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# =========================
# LOAD ENV
# =========================
load_dotenv()

# =========================
# APP SETUP
# =========================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# REQUEST MODEL
# =========================
class ChatRequest(BaseModel):
    message: str

# =========================
# API KEY
# =========================
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# =========================
# AI FUNCTION
# =========================
def query_ai(prompt):
    try:
        if not OPENROUTER_API_KEY:
            return "ERROR: API key not found. Check Render ENV."

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://your-app.onrender.com",  # optional but recommended
                "X-Title": "AI Career Counselor"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a helpful career counselor."},
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=30
        )

        data = response.json()
        print("API RESPONSE:", data)

        if response.status_code != 200:
            return f"API Error ({response.status_code}): {data}"

        if "choices" in data:
            return data["choices"][0]["message"]["content"]

        return "Unexpected AI response: " + str(data)

    except Exception as e:
        print("ERROR:", e)
        return "Error connecting to AI service."

# =========================
# MAIN LOGIC
# =========================
def get_response(user_input):
    prompt = f"""
Give short, clear, and helpful career advice.

User Question:
{user_input}
"""
    return query_ai(prompt)

# =========================
# ROUTES
# =========================
@app.get("/")
def root():
    return {"message": "AI Career Counselor Backend is running 🚀"}

@app.post("/chat")
def chat(request: ChatRequest):
    return {"reply": get_response(request.message)}