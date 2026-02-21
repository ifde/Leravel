import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Laravel API base URL
LARAVEL_API_URL = os.environ.get('LARAVEL_API_URL', 'http://localhost')
API_KEY = os.environ.get('TELEGRAM_PARSER_API_KEY', '')

# List of JSON files to load
JSON_FILES = [
    'hh_vacancies_scraped.json',
    'hirify_vacancies_scraped.json',
    'remocate_vacancies_scraped.json',
    'telegram_vacancies_scraped.json'
]

def load_vacancies_from_json(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            vacancies = json.load(f)
        print(f"Loaded {len(vacancies)} vacancies from {json_file}")
        return vacancies
    except FileNotFoundError:
        print(f"File {json_file} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding {json_file}.")
        return []

def save_vacancy_to_db(vacancy):
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
            return True
        else:
            print(f"Error {response.status_code}: {response.text}")
            return False
                    
    except Exception as e:
        print(f"Failed to save vacancy: {e}")
        return False

def main():
    total_saved = 0
    for json_file in JSON_FILES:
        vacancies = load_vacancies_from_json(json_file)
        for vacancy in vacancies:
            if save_vacancy_to_db(vacancy):
                total_saved += 1
    print(f"Total vacancies saved: {total_saved}")

if __name__ == '__main__':
    main()