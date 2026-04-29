import requests
from bs4 import BeautifulSoup

# Step 1: Fetch the page
url = "http://quotes.toscrape.com"
response = requests.get(url)

# Step 2: Parse the HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Step 3: Find all quote blocks
quotes = soup.find_all('div', class_='quote')

# Step 4: Loop through and extract text + author
for quote in quotes:
    text = quote.find('span', class_='text').text
    author = quote.find('small', class_='author').text
    print(f"{text} — {author}")