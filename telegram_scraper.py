import asyncio
import json  # Add json import
import requests
from datetime import datetime
from telethon import TelegramClient
from telethon import functions
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
MESSAGE_LIMIT = os.environ.get('MAX_CARDS_PER_PAGE', 100)

async def collect_messages():
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
    
    saved_vacancies = []  # List to collect saved vacancies
    
    for channel in CHANNELS:
        print(f"Collecting messages from {channel}...")
        try:
            chat = await client.get_entity(channel)
            
            # Fetch messages
            messages = await client.get_messages(chat, limit=MESSAGE_LIMIT)
            
            for message in messages:
                if message.message and 'php' in message.message.lower():  # Filter for PHP-related messages
                    # Parse title and description
                    lines = message.message.split('\n')
                    title = lines[0] if lines else message.message[:50]

                    if (not('php' in title.lower())): # If PHP is not in the title, skip
                        continue

                    description = message.message
                    
                    # Generate URL
                    url = f"https://t.me/{channel}/{message.id}"
                    
                    # Posted at
                    posted_at = message.date
                    
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
                    
                    if shared.send_vacancy_to_db(vacancy):  # Use shared script
                        saved_vacancies.append(vacancy)
        
        except Exception as e:
            print(f"Failed to collect from {channel}: {e}")
    
    # Save to JSON
    with open('telegram_vacancies_scraped.json', 'w', encoding='utf-8') as f:
        json.dump(saved_vacancies, f, ensure_ascii=False, indent=4)
    
    print("Collection complete!")

if __name__ == '__main__':
    asyncio.run(collect_messages())