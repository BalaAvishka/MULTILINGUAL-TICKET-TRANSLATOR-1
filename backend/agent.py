"""
Agent Loop: processes tickets through a series of steps.
Each step is recorded for transparency and demonstration of the Agent Loop capability.
"""
import uuid
from translator import detect_language, translate_to_english, translate_from_english
from glossary import apply_glossary, restore_glossary
from storage import save_ticket, get_ticket

def process_ticket_agent(ticket_text: str) -> dict:
    """
    Agent Loop Steps:
    1. Generate ticket ID
    2. Detect language
    3. Decide if translation is needed
    4. Apply glossary protection
    5. Translate to English
    6. Restore glossary terms
    7. Store both versions
    """
    ticket_id = str(uuid.uuid4())[:8]
    steps = []

    # Step 1: Detect language
    lang = detect_language(ticket_text)
    steps.append({"step": "detect_language", "result": lang})

    # Step 2: Decide translation
    if lang == 'en':
        english_text = ticket_text
        steps.append({"step": "translation_needed", "result": "false - already english"})
    else:
        steps.append({"step": "translation_needed", "result": "true"})

        # Step 3: Protect technical terms
        protected_text, placeholders = apply_glossary(ticket_text)
        steps.append({"step": "glossary_protection", "result": f"{len(placeholders)} terms protected"})

        # Step 4: Translate
        translated = translate_to_english(protected_text, lang)
        steps.append({"step": "translate_to_english", "result": "done"})

        # Step 5: Restore terms
        english_text = restore_glossary(translated, placeholders)
        steps.append({"step": "restore_glossary", "result": "done"})

    # Step 6: Store
    record = {
        "ticket_id": ticket_id,
        "original_lang": lang,
        "original_text": ticket_text,
        "english_text": english_text,
        "agent_steps": steps,
        "status": "open"
    }
    save_ticket(ticket_id, record)
    steps.append({"step": "store_ticket", "result": f"saved as {ticket_id}"})
    record["agent_steps"] = steps
    save_ticket(ticket_id, record)

    return record

def reply_to_user(ticket_id: str, english_reply: str) -> dict:
    """Translate engineer's English reply back to the ticket's original language."""
    ticket = get_ticket(ticket_id)
    if not ticket:
        raise ValueError(f"Ticket {ticket_id} not found")

    original_lang = ticket["original_lang"]

    if original_lang == 'en':
        final_reply = english_reply
    else:
        protected, placeholders = apply_glossary(english_reply)
        translated = translate_from_english(protected, original_lang)
        final_reply = restore_glossary(translated, placeholders)

    ticket["engineer_reply_english"] = english_reply
    ticket["engineer_reply_original"] = final_reply
    ticket["status"] = "replied"
    save_ticket(ticket_id, ticket)

    return {
        "ticket_id": ticket_id,
        "original_lang": original_lang,
        "english_reply": english_reply,
        "translated_reply": final_reply
    }
