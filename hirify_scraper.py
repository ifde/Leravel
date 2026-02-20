# hirify_scraper.py
import asyncio
import json
import random
import shared
import re
from datetime import datetime, timedelta
from playwright.async_api import async_playwright

# Base search URL without page
BASE_SEARCH_URL = "https://hirify.me/?params=title,company&period=month&search=PHP&skills=php&work_format=remote"

MAX_PAGE_COUNT=1
MAX_CARDS_PER_PAGE=8

UNIT_MAP = {
    'минут': 'minute',
    'часов': 'hour',
    'час': 'hour',
    'дней': 'day',
    'день': 'day'
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
        title = await detail_page.locator('h1').inner_text() if await detail_page.locator('h1').count() > 0 else None
        
        # Extract salary
        salary = await detail_page.locator('.font-bold.text-\\[28px\\]').inner_text() if await detail_page.locator('.font-bold.text-\\[28px\\]').count() > 0 else None
        
        # Extract grade
        grade = await detail_page.locator('.common-detail-item .label:has-text("Grade") + .value').inner_text() if await detail_page.locator('.common-detail-item .label:has-text("Grade")').count() > 0 else None

        # Extract country
        country = await detail_page.locator('.common-detail-item .label:has-text("Country") + .value').inner_text() if await detail_page.locator('.common-detail-item .label:has-text("Country")').count() > 0 else None
        
        # Extract tags (skills)
        tags = []
        tag_elements = detail_page.locator('.vacancy-detail-tags .tag')
        count = await tag_elements.count()
        for i in range(count):
            tag = await tag_elements.nth(i).inner_text()
            tags.append(tag)
        
        # Extract posted_at
        posted_at_locator = detail_page.locator('.font-light.text-\\[14px\\].text-tertiary')
        posted_at_text = await posted_at_locator.inner_text() if await posted_at_locator.count() > 0 else None
        posted_at = None
        if posted_at_text:
            # Parse "1 hour ago", "updated 6 hours ago", "1 day ago", etc.
            match = re.search(r'(?:обновлено\s+)?(\d+)\s+(\w+)\s+назад', posted_at_text.lower())
            if match:
                num, unit_ru = int(match.group(1)), match.group(2)
                unit = UNIT_MAP.get(unit_ru, unit_ru)
                delta = timedelta(hours=num) if unit == 'hour' else timedelta(days=num) if unit == 'day' else timedelta(minutes=num)
                posted_at = (datetime.now() - delta).isoformat()
                print(f"Date inserted: {posted_at}")
        
        # Extract description
        description_element = detail_page.locator('.description')
        description = await description_element.inner_html() if await description_element.count() > 0 else None
        
        return {
            'title': title,
            'salary': salary,
            'description': description,
            'grade': grade,
            'url': url,
            'company': None,  # Not extracted, will be null
            'logo': None,  # No logos
            'skills': tags,
            'experience': None,  # Not extracted, will be null
            'country': country,
            'source': 'hirify',
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
            locale='en_US',
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        page = await context.new_page()
        
        try:
            # Go to first page to get max pages
            first_url = f"{BASE_SEARCH_URL}&page=0"
            await page.goto(first_url, timeout=60000)
            await simulate_human_behavior(page)
            
            # Find max page number from pagination buttons
            page_buttons = page.locator('button[data-slot="pagination-item"]')
            max_page = await page_buttons.count()
            print(f"Total pages: {max_page}")
            
            vacancies = []
            for page_num in range(min(max_page, MAX_PAGE_COUNT)):  # Limit to 1 pagee for testing
                if page_num > 0:
                    search_url = f"{BASE_SEARCH_URL}&page={page_num}"
                    await page.goto(search_url, timeout=60000)
                    await simulate_human_behavior(page)
                
                # Find job links on current page
                job_links = page.locator('a.vacancy-card-link')
                count = await job_links.count()
                print(f"Page {page_num + 1}: Found {count} jobs")

                flag = True
                for i in range(min(count, MAX_CARDS_PER_PAGE)):
                    link_element = job_links.nth(i)
                    href = await link_element.get_attribute('href')
                    url = f"https://hirify.me{href}"  # Full URL
                    print(f"Scraping: {url}")
                    
                    vacancy_data = await scrape_vacancy_details(context, url)  # Pass context to open new page
                    if vacancy_data:
                        if shared.send_vacancy_to_db(vacancy_data):
                            vacancies.append(vacancy_data)
                        else:
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
            with open('hirify_vacancies_scraped.json', 'w', encoding='utf-8') as f:
                json.dump(vacancies, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error during main scraping: {e}")
        finally:
            await browser.close()

if __name__ == '__main__':
    asyncio.run(main())