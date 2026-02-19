# hh_scraper.py
import asyncio
import json
import random
import time
from playwright.async_api import async_playwright

SEARCH_URL = "https://hh.ru/search/vacancy?text=PHP&excluded_text=&professional_role=96&salary=&salary=&currency_code=RUR&experience=doesNotMatter&work_format=REMOTE&order_by=publication_time&search_period=0&items_on_page=50&L_save_area=true&page=2&search_session_id=62842306-89f2-4ac4-91f7-6135fc6f48e7"

async def simulate_human_behavior(page):
    # Random scroll and mouse movement
    await page.mouse.move(random.randint(100, 800), random.randint(100, 600))
    await page.evaluate("window.scrollTo(0, window.innerHeight / 2);")
    await asyncio.sleep(random.uniform(1, 3))
    await page.evaluate("window.scrollTo(0, window.innerHeight);")
    await asyncio.sleep(random.uniform(2, 5))

async def scrape_vacancy_details(page, url):
    await page.goto(url)
    await simulate_human_behavior(page)
    
    # Extract basic info
    title = await page.locator('h1[data-qa="vacancy-title"]').inner_text()
    salary = await page.locator('[data-qa="vacancy-salary"]').inner_text() if await page.locator('[data-qa="vacancy-salary"]').count() > 0 else None
    experience = await page.locator('[data-qa="vacancy-experience"]').inner_text() if await page.locator('[data-qa="vacancy-experience"]').count() > 0 else None
    
    # Extract description
    description_element = page.locator('[data-qa="vacancy-description"]')
    description = await description_element.inner_text() if await description_element.count() > 0 else None
    
    # Extract skills
    skills = []
    skill_elements = page.locator('[data-qa="skills-element"] .magritte-tag__label___YHV-o_5-1-1')
    count = await skill_elements.count()
    for i in range(count):
        skill = await skill_elements.nth(i).inner_text()
        skills.append(skill)
    
    return {
        'title': title,
        'salary': salary,
        'experience': experience,
        'description': description,
        'skills': skills,
        'url': url
    }

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set to True for headless
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        page = await context.new_page()
        
        await page.goto(SEARCH_URL)
        await simulate_human_behavior(page)
        
        # Find job links
        job_links = page.locator('a[data-qa="serp-item__title"]')
        count = await job_links.count()
        print(f"Found {count} jobs")
        
        vacancies = []
        for i in range(min(count, 5)):  # Limit to 5 for testing
            link_element = job_links.nth(i)
            url = await link_element.get_attribute('href')
            print(f"Scraping: {url}")
            
            vacancy_data = await scrape_vacancy_details(page, url)
            vacancies.append(vacancy_data)
            
            # Random delay between jobs
            await asyncio.sleep(random.uniform(5, 10))
        
        # Save to JSON
        with open('hh_vacancies_scraped.json', 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=4)
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())