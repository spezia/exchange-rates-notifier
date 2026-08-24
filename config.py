import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(BASE_DIR, ".env"))

def require(name: str) -> str:
    """Return an environment variable, or fail"""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required variable {name} in .env")
    return value

SMTP = {
    "server": require("SMTP_SERVER"),
    "port": int(require("SMTP_PORT")),
    "sender": require("EMAIL_SENDER"),
    "password": require("EMAIL_PASSWORD"),
    "receiver": require("EMAIL_RECEIVER"),
}

API = {
    "key": require("EXCHANGE_API_KEY"),
    "url": require("EXCHANGE_URL"),
    "currencies": [c.strip().upper() for c in require("LIST_CURRENCIES").split(",")],
}

def_currency = os.getenv("DEF_CURRENCY", "USD")
