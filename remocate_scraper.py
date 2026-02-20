# remocate_scraper.py
import asyncio
import json
import random
import re
import requests
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
import shared

# This is somewhat special
# It has infinite scroll
# Plus you got to pause the Playwright script to manyally type filters
# Otherwise there's some weird anibot scrolling

BASE_URL = "https://www.remocate.app"
MAX_SCROLL_ROUNDS = 1
MAX_CARDS_PER_PAGE=8

async def simulate_human_behavior(page):
    await page.mouse.move(random.randint(100, 800), random.randint(100, 600))
    await asyncio.sleep(random.uniform(2, 5))

async def scrape_vacancy_details(context, url, country):
    detail_page = await context.new_page()
    try:
        await detail_page.goto(url, timeout=60000)

        title = await detail_page.locator('.top-title-job').inner_text() if await detail_page.locator('.top-title-job').count() > 0 else None
        company = await detail_page.locator('.job-top-company').inner_text() if await detail_page.locator('.job-top-company').count() > 0 else None

        print(f"Company: {company}")

        # Extract logo
        logo_src = await detail_page.locator('.job-top-logo').get_attribute('src') if await detail_page.locator('.job-top-logo').count() > 0 else None
        logo = None
        if logo_src:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(logo_src, headers=headers, timeout=10)
                if response.status_code == 200:
                    safe_company = re.sub(r'[^\w\-_\.]', '_', company or 'unknown').lower()
                    filename = f"logos/{safe_company}.png"
                    with open(f"telegram-parser/storage/app/public/{filename}", 'wb') as f:
                        f.write(response.content)
                    logo = filename
                else:
                    print(f"Logo download failed: {response.status_code}")
            except Exception as e:
                print(f"Failed to download logo: {e}")
        
        # Extract posted_at
        posted_at_locator = detail_page.locator('.job-date.is-cms')
        posted_at_text = await posted_at_locator.inner_text() if await posted_at_locator.count() > 0 else None
        posted_at = None
        if posted_at_text:
            try:
                # Try "Feb 16, 2026" format
                posted_at = datetime.strptime(posted_at_text, "%b %d, %Y").isoformat()
            except ValueError:
                # Try "X days ago" format
                match = re.search(r'(\d+)\s+days?\s+ago', posted_at_text.lower())
                if match:
                    days = int(match.group(1))
                    posted_at = (datetime.now() - timedelta(days=days)).isoformat()

        tags = []
        tag_elements = detail_page.locator('.job-top-tags .job-tag')
        count = await tag_elements.count()
        for i in range(count):
            tag = await tag_elements.nth(i).inner_text()
            tags.append(tag)

        description_element = detail_page.locator('.text-rich-text')
        description = await description_element.inner_html() if await description_element.count() > 0 else None

        return {
            'title': title,
            'company': company,
            'skills': [],
            'description': description,
            'logo': logo,
            'url': url,
            'source': 'remocate',
            'country': country,  # note: add DB field if you want to persist
            'posted_at': posted_at
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
    finally:
        await detail_page.close()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        page = await context.new_page()

        try:
            await page.goto(BASE_URL, timeout=60000)

            # Manual filters
            await page.pause()

            await page.wait_for_selector('a.job-card', timeout=60000)

            seen_urls = set()
            saved_vacancies = []
            no_new_rounds = 0

            for _ in range(MAX_SCROLL_ROUNDS):
                job_cards = page.locator('a.job-card')
                count = await job_cards.count()
                print(f"Found {count} cards")

                flag = True
                for i in range(min(count, MAX_CARDS_PER_PAGE)):
                    card = job_cards.nth(i)
                    href = await card.get_attribute('href')
                    if not href:
                        continue
                    url = f"https://www.remocate.app{href}"
                    if url in seen_urls:
                        continue
                    seen_urls.add(url)

                    # Country from card
                    country_locator = card.locator('.job-card_tag[fs-cmsfilter-field="location"]')
                    country = await country_locator.inner_text() if await country_locator.count() > 0 else None

                    vacancy_data = await scrape_vacancy_details(context, url, country)
                    if vacancy_data:
                        if shared.send_vacancy_to_db(vacancy_data):
                            saved_vacancies.append(vacancy_data)
                        else:
                            flag = False
                            break

                if not flag:
                    break

                # Scroll to load more
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                await asyncio.sleep(random.uniform(2, 4))

            # Save only newly saved vacancies
            with open('remocate_vacancies_scraped.json', 'w', encoding='utf-8') as f:
                json.dump(saved_vacancies, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error during main scraping: {e}")
        finally:
            await browser.close()

if __name__ == '__main__':
    asyncio.run(main())