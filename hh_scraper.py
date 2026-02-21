# hh_scraper.py
import asyncio
import json
import random
import re  # Add for regex matching
import os
from dotenv import load_dotenv
import requests
import shared
from datetime import datetime
from playwright.async_api import async_playwright

load_dotenv()

# Base search URL without page
BASE_SEARCH_URL = "https://hh.ru/search/vacancy?text=PHP&professional_role=96&work_format=REMOTE&per_page=200&order_by=publication_time"

MAX_PAGE_COUNT = int(os.environ.get('MAX_PAGE_COUNT', 100))
MAX_CARDS_PER_PAGE = int(os.environ.get('MAX_CARDS_PER_PAGE', 100))
SAVE_ONLY_NEW = int(os.environ.get('SAVE_ONLY_NEW', 0))

print(f"Starting the hh_scraper script")
print(f"MAX_PAGE_COUNT: {MAX_PAGE_COUNT}")
print(f"MAX_CARDS_PER_PAGE: {MAX_CARDS_PER_PAGE}")
print(f"SAVE_ONLY_NEW: {SAVE_ONLY_NEW}")

# Ensure logos folder exists
os.makedirs('telegram-parser/storage/app/public/logos', exist_ok=True)

MONTH_MAP = {
    'января': 'January',
    'февраля': 'February',
    'марта': 'March',
    'апреля': 'April',
    'мая': 'May',
    'июня': 'June',
    'июля': 'July',
    'августа': 'August',
    'сентября': 'September',
    'октября': 'October',
    'ноября': 'November',
    'декабря': 'December'
}

async def simulate_human_behavior(page):
    # Random scroll and mouse movement
    await page.mouse.move(random.randint(100, 800), random.randint(100, 600))
    await page.evaluate("window.scrollTo(0, window.innerHeight / 2);")
    await asyncio.sleep(random.uniform(1, 3))
    await page.evaluate("window.scrollTo(0, window.innerHeight);")
    await asyncio.sleep(random.uniform(2, 5))

async def scrape_vacancy_details(context, url):
    detail_page = await context.new_page()  # Open in new tab (new page)
    try:
        await detail_page.goto(url, timeout=60000)
        # await simulate_human_behavior(detail_page)
        
        # Extract title
        title = await detail_page.locator('h1[data-qa="vacancy-title"]').inner_text() if await detail_page.locator('h1[data-qa="vacancy-title"]').count() > 0 else None

        # Extract posted_at
        posted_at_locator = detail_page.locator('.magritte-text_style-secondary___1IU11_4-5-0').filter(has_text="Вакансия опубликована")
        posted_at_text = await posted_at_locator.inner_text() if await posted_at_locator.count() > 0 else None
        posted_at = None
        if posted_at_text:
            match = re.search(r'(\d{1,2})\s+(\w+)\s+(\d{4})', posted_at_text)
            if match:
                day, month_ru, year = match.groups()
                month_en = MONTH_MAP.get(month_ru.lower())
                if month_en:
                    try:
                        posted_at = datetime.strptime(f"{day} {month_en} {year}", "%d %B %Y").isoformat()
                    except ValueError:
                        pass
        
        # Parse grade from title
        grade = None
        if title:
            title_lower = title.lower()
            if re.search(r'\b(senior|sr\.?)\b', title_lower):
                grade = "Senior"
            elif re.search(r'\b(middle|mid\.?)\b', title_lower):
                grade = "Middle"
            elif re.search(r'\b(junior|jr\.?)\b', title_lower):
                grade = "Junior"
        
        # Extract salary
        salary = await detail_page.locator('[data-qa="vacancy-salary"]').inner_text() if await detail_page.locator('[data-qa="vacancy-salary"]').count() > 0 else None
        
        # Extract company name
        company = await detail_page.locator('[data-qa="vacancy-company-name"]').inner_text() if await detail_page.locator('[data-qa="vacancy-company-name"]').count() > 0 else None
        
        # Extract company logo
        logo_src = await detail_page.locator('[data-qa="vacancy-company-logo"] img').get_attribute('src') if await detail_page.locator('[data-qa="vacancy-company-logo"] img').count() > 0 else None
        print(f"Logo src: {logo_src}")  # Debug
        logo = None
        if logo_src:
            if not logo_src.startswith('http'):
                logo_src = f"https://hh.ru{logo_src}"
            print(f"Full logo URL: {logo_src}")  # Debug
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(logo_src, headers=headers, timeout=10)
                print(f"Response status: {response.status_code}")  # Debug
                if response.status_code == 200:
                    safe_company = re.sub(r'[^\w\-_\.]', '_', company or 'unknown').lower()
                    filename = f"logos/{safe_company}.png"  # Add random to avoid overwrites
                    with open(f"telegram-parser/storage/app/public/{filename}", 'wb') as f:
                        f.write(response.content)
                    logo = filename
                    print(f"Logo saved: {filename}")  # Debug
                else:
                    print(f"Download failed: {response.status_code}")
            except Exception as e:
                print(f"Failed to download logo: {e}")
        
        # Extract experience
        experience = await detail_page.locator('[data-qa="vacancy-experience"]').inner_text() if await detail_page.locator('[data-qa="vacancy-experience"]').count() > 0 else None
        
        # Extract description
        description_element = detail_page.locator('[data-qa="vacancy-description"]')
        description = await description_element.inner_text() if await description_element.count() > 0 else None
        
        # Extract skills
        skills = []
        skill_elements = detail_page.locator('[data-qa="skills-element"] .magritte-tag__label___YHV-o_5-1-1')
        count = await skill_elements.count()
        for i in range(count):
            skill = await skill_elements.nth(i).inner_text()
            skills.append(skill)
        
        return {
            'title': title,
            'salary': salary,
            'company': company,
            'logo': logo,
            'description': description,
            'grade': grade,  # Now parsed from title
            'skills': skills,
            'experience': experience,
            'url': url,
            'country': 'Russia',
            'source': 'hh',
            'posted_at': posted_at
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
    finally:
        await detail_page.close()  # Close the new tab after scraping

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        page = await context.new_page()
        
        try:
            # Go to first page to get max pages
            first_url = f"{BASE_SEARCH_URL}&page=0"
            await page.goto(first_url, timeout=60000)
            await simulate_human_behavior(page)
            
            # Find max page number
            page_links = page.locator('a[data-qa="pager-page"]')
            max_page = await page_links.count()
            print(f"Total pages: {max_page}")
            
            vacancies = []
            for page_num in range(min(max_page, MAX_PAGE_COUNT)):
                if page_num > 0:
                    search_url = f"{BASE_SEARCH_URL}&page={page_num}"
                    await page.goto(search_url, timeout=60000)
                    await simulate_human_behavior(page)
                
                # Find job links on current page
                job_links = page.locator('a[data-qa="serp-item__title"]')
                count = await job_links.count()
                print(f"Page {page_num + 1}: Found {count} jobs")

                flag = True
                for i in range(min(count, MAX_CARDS_PER_PAGE)): # 8 jobs for testing
                    link_element = job_links.nth(i)
                    url = await link_element.get_attribute('href')
                    print(f"Scraping: {url}")
                    
                    vacancy_data = await scrape_vacancy_details(context, url)  # Pass context to open new page
                    if vacancy_data:
                        if shared.send_vacancy_to_db(vacancy_data):
                            vacancies.append(vacancy_data)
                        else:
                            if SAVE_ONLY_NEW:
                                flag = False
                                break
                    
                    if not flag:
                        break
                    
                    # Random delay between jobs
                    # await asyncio.sleep(random.uniform(1, 3))
                
                if not flag:
                    print("No new vacancies on this page, stopping")
                    break
                
                # Delay between pages
                # await asyncio.sleep(random.uniform(5, 10))
            
            # Save to JSON
            with open('hh_vacancies_scraped.json', 'w', encoding='utf-8') as f:
                json.dump(vacancies, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error during main scraping: {e}")
        finally:
            await browser.close()

if __name__ == '__main__':
    asyncio.run(main())