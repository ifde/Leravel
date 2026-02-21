import subprocess
import json
from datetime import datetime

scrapers = [
    ('hh_scraper.py', 'hh_vacancies_scraped.json'),
    ('hirify_scraper.py', 'hirify_vacancies_scraped.json'),
    ('remocate_scraper.py', 'remocate_vacancies_scraped.json'),
    ('telegram_scraper.py', 'telegram_vacancies_scraped.json')
]

# Load existing log
try:
    with open('log.json', 'r') as f:
        log_data = json.load(f)
except FileNotFoundError:
    log_data = []

for scraper, json_file in scrapers:
    print(f"Running {scraper}")
    subprocess.run(['python', scraper])
    
    saved_urls = []
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            vacancies = json.load(f)
        saved_urls = [v['url'] for v in vacancies]
    except FileNotFoundError:
        print(f"File {json_file} not found.")
    
    new_saves = len(saved_urls)
    print(f"{scraper}: {new_saves} saved")
    for url in saved_urls:
        print(url)
    
    # Add to log
    log_entry = {
        "date": datetime.now().isoformat(),
        "scraper": scraper,
        "saved": new_saves,
        "urls": saved_urls
    }
    log_data.append(log_entry)

# Save log
with open('log.json', 'w') as f:
    json.dump(log_data, f, indent=4)