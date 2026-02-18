import psycopg2
import asyncio
import requests
from datetime import datetime
from telethon import TelegramClient, events
from dotenv import load_dotenv
import os

load_dotenv()

api_id = os.environ['TELEGRAM_API_ID']
api_hash = os.environ['TELEGRAM_API_HASH']
client = TelegramClient('anon', api_id, api_hash)

# Use the same credentials as in your Laravel .env
conn = psycopg2.connect(
    dbname="laravel",
    user="sail",
    password="password",
    host="127.0.0.1",  # or '127.0.0.1'
    port=5432
)

def save_message(channel, message, posted_at):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO telegram_messages (channel, message, posted_at, created_at, updated_at) " \
            "VALUES (%s, %s, %s, %s, %s)"
            "RETURNING id",
            (channel, message, posted_at, datetime.now(), datetime.now())
        )
        conn.commit()

        new_id = cur.fetchone()[0]
        conn.commit()
    
    try:
        # Use 'http://localhost' if running on host, or 'http://laravel.test' for Sail
        laravel_api_url = "http://localhost/api/broadcast-telegram-message"
        response = requests.post(laravel_api_url, data={'message_id': new_id})
        print(response.status_code) # If this is 419, it's CSRF. If 404, it's the route path.
        print("Message sent to the website wow!")
    except Exception as e:
        print(f"Failed to notify Laravel: {e}")


@client.on(events.NewMessage(incoming=True))
async def handler(event):
    chat = await event.get_chat()
    channel = getattr(chat, 'ifdeifde', 'private_user')
    channel = event.chat.username if event.chat else 'unknown'
    message = event.message.message
    posted_at = event.message.date
    await asyncio.to_thread(save_message, channel, message, posted_at)

with client:
    client.run_until_disconnected()