import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(BASE_DIR, ".env"))

SMTP = {
    "server": os.getenv("SMTP_SERVER"),
    "port": int(os.getenv("SMTP_PORT")),
    "sender": os.getenv("EMAIL_SENDER"),
    "password": os.getenv("EMAIL_PASSWORD"),
    "receiver": os.getenv("EMAIL_RECEIVER"),
}

API = {
    "key": os.getenv("EXCHANGE_API_KEY"),
    "url": os.getenv("EXCHANGE_URL"),
    "currencies": os.getenv("LIST_CURRENCIES").split(","),
}

def_currency = os.getenv("DEF_CURRENCY", "USD")