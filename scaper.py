import requests
from bs4 import BeautifulSoup
import csv

base_url = "http://quotes.toscrape.com/page/{}/"
all_quotes = []

print("Starting scraper...")

for page_num in range(1, 11):
    url = base_url.format(page_num)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = soup.find_all('div', class_='quote')

    if not quotes:
        print(f"No more pages found at page {page_num}. Stopping.")
        break

    for quote in quotes:
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        tags = [t.text for t in quote.find_all('a', class_='tag')]

        all_quotes.append({
            'text': text,
            'author': author,
            'tags': ', '.join(tags)
        })

    print(f"Page {page_num} scraped — {len(quotes)} quotes found")

# Save to CSV
with open('quotes.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['text', 'author', 'tags'])
    writer.writeheader()
    writer.writerows(all_quotes)

print(f"\nDone! Total quotes scraped: {len(all_quotes)}")
print("Saved to quotes.csv — check your python folder!")