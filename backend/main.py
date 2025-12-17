from fastapi import FastAPI
from pydantic import BaseModel
from agent import ask_agent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    message: str

@app.post("/chat")
def chat(query: Query):
    try:
        response = ask_agent(query.message)
        return {"reply": response}
    except Exception as e:
        print("Backend Error:", e)
        return {"reply": "Server error occurred."}

