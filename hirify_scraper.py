# hirify_scraper.py
import asyncio
import json
import random
from playwright.async_api import async_playwright

SEARCH_URL = "https://hirify.me/?params=title,company&period=month&search=PHP&skills=php&work_format=remote"

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
    
    # Extract title
    title = await page.locator('h1').inner_text() if await page.locator('h1').count() > 0 else None
    
    # Extract salary
    salary = await page.locator('.font-bold.text-\\[28px\\]').inner_text() if await page.locator('.font-bold.text-\\[28px\\]').count() > 0 else None
    
    # Extract work format
    work_format = await page.locator('.common-detail-item .label:has-text("Work format") + .value').inner_text() if await page.locator('.common-detail-item .label:has-text("Work format")').count() > 0 else None
    
    # Extract work type
    work_type = await page.locator('.common-detail-item .label:has-text("Work type") + .value').inner_text() if await page.locator('.common-detail-item .label:has-text("Work type")').count() > 0 else None
    
    # Extract grade
    grade = await page.locator('.common-detail-item .label:has-text("Grade") + .value').inner_text() if await page.locator('.common-detail-item .label:has-text("Grade")').count() > 0 else None
    
    # Extract country
    country = await page.locator('.common-detail-item .label:has-text("Country") + .value').inner_text() if await page.locator('.common-detail-item .label:has-text("Country")').count() > 0 else None
    
    # Extract tags (skills)
    tags = []
    tag_elements = page.locator('.vacancy-detail-tags .tag')
    count = await tag_elements.count()
    for i in range(count):
        tag = await tag_elements.nth(i).inner_text()
        tags.append(tag)
    
    # Extract description
    description_element = page.locator('.description')
    description = await description_element.inner_html() if await description_element.count() > 0 else None
    
    return {
        'title': title,
        'salary': salary,
        'work_format': work_format,
        'work_type': work_type,
        'grade': grade,
        'country': country,
        'tags': tags,
        'description': description,
        'url': url
    }

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        page = await context.new_page()
        
        await page.goto(SEARCH_URL)
        await simulate_human_behavior(page)
        
        # Find job links
        job_links = page.locator('a.vacancy-card-link')
        count = await job_links.count()
        print(f"Found {count} jobs")
        
        vacancies = []
        for i in range(min(count, 5)):  # Limit to 5 for testing
            link_element = job_links.nth(i)
            href = await link_element.get_attribute('href')
            url = f"https://hirify.me{href}"  # Full URL
            print(f"Scraping: {url}")
            
            vacancy_data = await scrape_vacancy_details(page, url)
            vacancies.append(vacancy_data)
            
            # Random delay between jobs
            await asyncio.sleep(random.uniform(5, 10))
        
        # Save to JSON
        with open('hirify_vacancies_scraped.json', 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=4)
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())