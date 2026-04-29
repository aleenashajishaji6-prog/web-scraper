from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv

# Set up Chrome browser automatically
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

print("Browser opened. Navigating to site...")
driver.get("http://books.toscrape.com")

# Wait until books are loaded on the page
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "product_pod"))
)

books = []

# Scrape 3 pages
for page in range(1, 4):
    print(f"Scraping page {page}...")

    items = driver.find_elements(By.CLASS_NAME, "product_pod")

    for item in items:
        title = item.find_element(By.TAG_NAME, 'h3').text
        price = item.find_element(By.CLASS_NAME, 'price_color').text
        rating = item.find_element(By.CLASS_NAME, 'star-rating').get_attribute('class').split()[-1]
        books.append({'title': title, 'price': price, 'rating': rating})

    # Click "next" button to go to next page
    try:
        next_btn = driver.find_element(By.CLASS_NAME, 'next')
        next_btn.find_element(By.TAG_NAME, 'a').click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product_pod"))
        )
    except:
        print("No more pages.")
        break

driver.quit()
print(f"\nDone! Scraped {len(books)} books.")

# Save to CSV
with open('books.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['title', 'price', 'rating'])
    writer.writeheader()
    writer.writerows(books)

print("Saved to books.csv!")