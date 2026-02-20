import requests
from dotenv import load_dotenv
import os

load_dotenv()

LARAVEL_API_URL = "http://localhost"
API_KEY = os.environ.get('TELEGRAM_PARSER_API_KEY', '')

def send_vacancy_to_db(vacancy):
    try:
        headers = {
            'X-API-Key': API_KEY,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.post(
            f"{LARAVEL_API_URL}/api/vacancies",
            json=vacancy,
            headers=headers
        )
        
        if response.status_code == 201:
            print(f"Vacancy saved! ID: {response.json()['id']}")
            return True  # New save
        elif response.status_code == 409:
            print(f"Vacancy already exists: {vacancy.get('url')}")
            return False  # Duplicate
        else:
            print(f"Error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"Failed to send vacancy: {e}")
        return False