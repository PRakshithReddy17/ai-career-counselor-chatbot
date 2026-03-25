from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from fastapi.middleware.cors import CORSMiddleware

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
# AI FUNCTION (OPENROUTER)
# =========================
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def query_ai(prompt):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
               "model": "openchat/openchat-7b:free",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )

        data = response.json()
        print("API RESPONSE:", data)

        if "choices" in data:
            return data["choices"][0]["message"]["content"]

        return "AI error: " + str(data)

    except Exception as e:
        print("ERROR:", e)
        return "Error connecting to AI service."

# =========================
# MAIN LOGIC
# =========================
def get_response(user_input):
    prompt = f"""
You are an AI career counselor.

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