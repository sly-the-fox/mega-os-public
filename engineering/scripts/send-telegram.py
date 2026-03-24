#!/usr/bin/env python3
"""Send a text file to Telegram. Usage: send-telegram.py <file_path>"""
import sys, os, httpx
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "telegram-bridge", ".env"))
token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("ALLOWED_CHAT_IDS")

if not token or not chat_id:
    print("Missing TELEGRAM_BOT_TOKEN or ALLOWED_CHAT_IDS")
    sys.exit(1)

msg = open(sys.argv[1]).read()
url = f"https://api.telegram.org/bot{token}/sendMessage"
chunks = [msg[i:i+4000] for i in range(0, len(msg), 4000)]
for chunk in chunks:
    r = httpx.post(url, json={"chat_id": int(chat_id), "text": chunk})
    data = r.json()
    print(f"Status: {r.status_code}, OK: {data.get('ok', False)}")
    if not data.get("ok"):
        print(f"Error: {data.get('description', 'unknown')}")
