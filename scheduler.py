import schedule
import time
import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

def run_scraper():
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Scraper started...")

    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT UNIQUE,
            author TEXT,
            tags TEXT,
            scraped_at TEXT
        )
    ''')

    base_url = "http://quotes.toscrape.com/page/{}/"
    new_count = 0

    for page_num in range(1, 11):
        url = base_url.format(page_num)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('div', class_='quote')

        if not quotes:
            break

        for quote in quotes:
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            tags = ', '.join([t.text for t in quote.find_all('a', class_='tag')])
            scraped_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute(
                "INSERT OR IGNORE INTO quotes (text, author, tags, scraped_at) VALUES (?, ?, ?, ?)",
                (text, author, tags, scraped_at)
            )
            if cursor.rowcount > 0:
                new_count += 1

    conn.commit()
    conn.close()
    print(f"Done! {new_count} new quotes saved.")
    print(f"Next run in 1 minute...")

# Run once immediately when script starts
run_scraper()

# Then schedule to run every 1 minute (change to .hours(1) for hourly)
schedule.every(1).minutes.do(run_scraper)

print("\nScheduler running... Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    time.sleep(1)