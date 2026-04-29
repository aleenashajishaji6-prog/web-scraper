import requests
from bs4 import BeautifulSoup
import sqlite3

# Set up database
conn = sqlite3.connect('quotes.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT UNIQUE,
        author TEXT,
        tags TEXT
    )
''')
conn.commit()
print("Database created!")

# Scrape all pages
base_url = "http://quotes.toscrape.com/page/{}/"
total_saved = 0

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

        try:
            cursor.execute(
                "INSERT OR IGNORE INTO quotes (text, author, tags) VALUES (?, ?, ?)",
                (text, author, tags)
            )
            if cursor.rowcount > 0:
                total_saved += 1
        except Exception as e:
            print(f"Skipped: {e}")

    print(f"Page {page_num} done")

conn.commit()
conn.close()
print(f"\nDone! {total_saved} quotes saved to quotes.db")
# Read back and display sample
conn = sqlite3.connect('quotes.db')
cursor = conn.cursor()
cursor.execute("SELECT author, text FROM quotes LIMIT 5")
rows = cursor.fetchall()
print("\nSample from database:")
for row in rows:
    print(f"  {row[0]}: {row[1][:60]}...")
conn.close()