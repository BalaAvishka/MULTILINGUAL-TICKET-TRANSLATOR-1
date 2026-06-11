from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from agent import process_ticket_agent, reply_to_user
from storage import list_tickets, get_ticket
import os

app = FastAPI(title="Multilingual Ticket Translator API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class TicketIn(BaseModel):
    text: str

class ReplyIn(BaseModel):
    ticket_id: str
    reply: str

@app.get("/health")
def health():
    return {"status": "ok", "message": "Multilingual Ticket Translator is running"}

@app.post("/translate")
def translate_ticket(ticket: TicketIn):
    if not ticket.text.strip():
        raise HTTPException(status_code=400, detail="Ticket text cannot be empty")
    result = process_ticket_agent(ticket.text)
    return result

@app.post("/reply")
def send_reply(data: ReplyIn):
    try:
        result = reply_to_user(data.ticket_id, data.reply)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/tickets")
def get_all_tickets():
    return list_tickets()

@app.get("/tickets/{ticket_id}")
def get_single_ticket(ticket_id: str):
    ticket = get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

# Serve frontend
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")
