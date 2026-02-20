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

# List of public channels to track (add usernames)
CHANNELS = ['setters', 'ifdeifde', 'ifdephpbot', 'onlyjohn111']

def save_message(channel, message, posted_at, profile_pic_path):
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
                'posted_at': posted_at.isoformat(),
                'profile_pic_path': profile_pic_path
            },
            headers=headers
        )
        
        if response.status_code == 201:
            print(f"Message saved! ID: {response.json()['id']}")
        else:
            print(f"Error {response.status_code}: {response.text}")
                    
    except Exception as e:
        print(f"Failed to notify Laravel: {e}")


@client.on(events.NewMessage(chats=CHANNELS))  # Only listen to specified channels
async def handler(event):
    chat = await event.get_chat()
    # get channel handle
    channel = chat.username or 'unknown'
    
    # Extra check (optional)
    if channel not in CHANNELS:
        return
    
    message = event.message.message
    posted_at = event.message.date
    
    # Get view count for the message
    # Only works for a user
    '''
    view_count = None
    try:
        views_result = await client(functions.messages.GetMessagesViewsRequest(
            peer=chat,
            id=[event.message.id],
            increment=False
        ))
        if views_result.views:
            view_count = views_result.views[0].views
    except Exception as e:
        print(f"Failed to get views: {e}")
    '''

    # Get profile picture
    profile_pic_path = None
    try:
        photos = await client.get_profile_photos(chat)
        if photos:
            os.makedirs('telegram-parser/storage/app/public/photos/', exist_ok=True)
            await client.download_media(photos[0], file=f'telegram-parser/storage/app/public/photos/{channel}.jpg')
            profile_pic_path = f'photos/{channel}.jpg'
    except Exception as e:
        print(f"Failed to download profile pic for {channel}: {e}")
    
    await asyncio.to_thread(save_message, channel, message, posted_at, profile_pic_path)


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
    print(f"Listening for new messages in channels: {', '.join(CHANNELS)}...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())