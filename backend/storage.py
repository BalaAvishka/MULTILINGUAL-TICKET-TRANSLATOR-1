import json, os

STORAGE_DIR = "tickets_store"
os.makedirs(STORAGE_DIR, exist_ok=True)

def save_ticket(ticket_id: str, data: dict):
    with open(f"{STORAGE_DIR}/{ticket_id}.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_ticket(ticket_id: str) -> dict:
    path = f"{STORAGE_DIR}/{ticket_id}.json"
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)

def list_tickets() -> list:
    tickets = []
    for file in sorted(os.listdir(STORAGE_DIR), reverse=True):
        if file.endswith(".json"):
            with open(f"{STORAGE_DIR}/{file}") as f:
                tickets.append(json.load(f))
    return tickets
