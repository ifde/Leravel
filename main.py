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

# Laravel API base URL
LARAVEL_API_URL = "http://localhost"  # or "http://laravel.test" for Sail
API_KEY = os.environ.get('TELEGRAM_PARSER_API_KEY', '')

def save_message(channel, message, posted_at):
    try:
        headers = {
            'X-API-Key': API_KEY,
            'Content-Type': 'application/json'
        }

        response = requests.post(
            f"{LARAVEL_API_URL}/api/post-telegram-message",
            json={
                'channel': channel,
                'message': message,
                'posted_at': posted_at.isoformat()
            },
            headers=headers
        )
        
        if response.status_code == 201:
            print(f"Message saved! ID: {response.json()['id']}")
        else:
            print(f"Error {response.status_code}: {response.json()}")
                    
    except Exception as e:
        print(f"Failed to notify Laravel: {e}")


@client.on(events.NewMessage(incoming=True))
async def handler(event):
    chat = await event.get_chat()
    channel = event.chat.username if event.chat else 'unknown'
    message = event.message.message
    posted_at = event.message.date
    
    await asyncio.to_thread(save_message, channel, message, posted_at)


with client:
    client.run_until_disconnected()