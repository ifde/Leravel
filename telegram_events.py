import asyncio
import requests
from datetime import datetime
from telethon import TelegramClient, events
from dotenv import load_dotenv
import os
import shared  # Import shared script

load_dotenv()

api_id = os.environ['TELEGRAM_API_ID']
api_hash = os.environ['TELEGRAM_API_HASH']
client = TelegramClient('anon', api_id, api_hash)

# Laravel API base URL
LARAVEL_API_URL = os.environ.get('LARAVEL_API_URL', 'http://localhost')
API_KEY = os.environ.get('TELEGRAM_PARSER_API_KEY', '')

# List of public channels to track (add usernames)
CHANNELS = ['setters', 'ifdeifde', 'ifdephpbot', 'onlyjohn111']

@client.on(events.NewMessage(chats=CHANNELS))  # Only listen to specified channels
async def handler(event):
    chat = await event.get_chat()
    channel = chat.username or 'unknown'
    
    if channel not in CHANNELS:
        return
    
    message_text = event.message.message
    if not message_text or 'php' not in message_text.lower():
        return  # Skip if no message or no PHP
    
    # Parse title and description
    lines = message_text.split('\n')
    title = lines[0] if lines else message_text[:50]
    
    if 'php' not in title.lower():  # Skip if PHP not in title
        return
    
    description = message_text
    
    # Generate URL
    url = f"https://t.me/{channel}/{event.message.id}"
    
    # Posted at
    posted_at = event.message.date
    
    vacancy = {
        'title': title,
        'company': None,
        'logo': None,
        'skills': [],
        'description': description,
        'url': url,
        'source': 'Telegram',
        'country': 'Global',
        'posted_at': posted_at.isoformat()
    }
    
    # Save to DB using shared script
    shared.send_vacancy_to_db(vacancy)
    print(f"Vacancy saved from {channel}!")

async def main():
    await client.connect()
    
    if not await client.is_user_authorized():
        print("Login required. Check your Telegram app for a code.")
        try:
            await client.start()
        except Exception:
            print("Phone code failed. Generating QR Code...")
            qr_login = await client.qr_login()
            print(f"Scan this URL in Telegram Settings > Devices: {qr_login.url}")
            await qr_login.wait()

    print("Successfully logged in as User!")
    print(f"Listening for new PHP-related messages in channels: {', '.join(CHANNELS)}...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())