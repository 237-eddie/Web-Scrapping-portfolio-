import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_quotes():
    quotes_data = []
    page = 1

    while True:
        url = f"http://quotes.toscrape.com/page/{page}/"
        response = requests.get(url)

        # Stop if the page doesn't load correctly
        if response.status_code != 200:
            print(f"Stopped at page {page} (status code {response.status_code})")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quote_blocks = soup.find_all("div", class_="quote")

        # Stop if there are no more quotes on this page
        if not quote_blocks:
            break

        for quote_block in quote_blocks:
            text = quote_block.find("span", class_="text").get_text()
            author = quote_block.find("small", class_="author").get_text()
            quotes_data.append([text, author])

        print(f"Scraped page {page} ({len(quote_blocks)} quotes)")
        page += 1

        time.sleep(1)  # be polite to the server - wait 1 second between requests

    return quotes_data

def save_to_csv(data, filename="quotes.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Quote", "Author"])
        writer.writerows(data)
    print(f"Saved {len(data)} quotes total to {filename}")

if __name__ == "__main__":
    quotes = scrape_quotes()
    save_to_csv(quotes)