from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from agent import handle_query

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "AI Agent Running"}

@app.post("/chat")
def chat(request: ChatRequest):

    user_message = request.message

    response = handle_query(user_message)

    return {
        "user": user_message,
        "response": response
    }