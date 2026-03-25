from fastapi import FastAPI
from pydantic import BaseModel
from backend import get_response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later we will restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Request(BaseModel):
    message: str

@app.post("/chat")
def chat(req: Request):
    reply = get_response(req.message)
    return {"reply": reply}