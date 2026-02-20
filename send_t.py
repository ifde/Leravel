import json
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import sys

load_dotenv()

LARAVEL_API_URL = "http://localhost"
API_KEY = os.environ.get('TELEGRAM_PARSER_API_KEY', '')

def vacancy_exists(url):
    try:
        response = requests.get(
            f"{LARAVEL_API_URL}/api/vacancies/check",
            params={'url': url},
            headers={'X-API-Key': API_KEY}
        )
        if response.status_code == 200:
            return response.json().get('exists', False)
        return False
    except Exception as e:
        print(f"Error checking vacancy: {e}")
        return False

def send_vacancy_to_db(vacancy):
    try:
        headers = {
            'X-API-Key': API_KEY,
            'Content-Type': 'application/json'
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

# Get file from argument
file = sys.argv[1] if len(sys.argv) > 1 else 'hh_vacancies_scraped.json'

new_count = 0
try:
    with open(file, 'r', encoding='utf-8') as f:
        vacancies = json.load(f)
    
    for vacancy in vacancies:
        url = vacancy.get('url')
        if vacancy_exists(url):
            print(f"Vacancy already exists: {url}")
            continue
        
        if send_vacancy_to_db(vacancy):
            new_count += 1
except FileNotFoundError:
    print(f"File {file} not found.")
except Exception as e:
    print(f"Error processing {file}: {e}")

print(f"NEW_SAVES: {new_count}")