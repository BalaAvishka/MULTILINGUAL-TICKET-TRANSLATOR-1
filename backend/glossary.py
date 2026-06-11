# Technical terms that must not be translated
GLOSSARY = {
    "ticket": "ticket",
    "API": "API",
    "login": "login",
    "logout": "logout",
    "dashboard": "dashboard",
    "error 404": "error 404",
    "error 500": "error 500",
    "OAuth": "OAuth",
    "JWT": "JWT",
    "SSL": "SSL",
    "webhook": "webhook",
    "endpoint": "endpoint",
    "token": "token",
    "password": "password",
    "username": "username",
    "URL": "URL",
    "HTTP": "HTTP",
    "HTTPS": "HTTPS",
    "JSON": "JSON",
    "CSV": "CSV",
}

def apply_glossary(text: str):
    placeholders = {}
    for i, (term, keep) in enumerate(GLOSSARY.items()):
        placeholder = f"__TERM{i}__"
        if term in text:
            text = text.replace(term, placeholder)
            placeholders[placeholder] = keep
    return text, placeholders

def restore_glossary(text: str, placeholders: dict) -> str:
    for placeholder, term in placeholders.items():
        text = text.replace(placeholder, term)
    return text
