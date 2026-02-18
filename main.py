import asyncio
import requests
from datetime import datetime
from telethon import TelegramClient, events
from telethon import functions, types
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
    result = await client(functions.channels.GetMessagesRequest(
        channel='setters',
        id=[42]
    ))
    print(result.stringify())

    last_message = (await client.get_messages('setters', 1))[0]

    print(last_message)

    full_channel = await client(functions.channels.GetFullChannelRequest('setters'))
    print(f"Subscribers: {full_channel.full_chat.participants_count}")

    chat = await event.get_chat()
    channel = event.chat.username if event.chat else 'unknown'
    message = event.message.message
    posted_at = event.message.date
    
    await asyncio.to_thread(save_message, channel, message, posted_at)


async def main():
    # Start the client with a more reliable login flow
    await client.connect()
    
    if not await client.is_user_authorized():
        print("Login required. Check your Telegram app for a code.")
        try:
            # Try standard login (Check your Telegram App for the code!)
            await client.start()
        except Exception:
            # Fallback to QR Code if phone code doesn't arrive/work
            print("Phone code failed. Generating QR Code...")
            qr_login = await client.qr_login()
            print(f"Scan this URL in Telegram Settings > Devices: {qr_login.url}")
            await qr_login.wait()

    print("Successfully logged in as User!")
    print("Listening for messages...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())