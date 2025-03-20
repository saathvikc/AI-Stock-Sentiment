import requests
from bs4 import BeautifulSoup
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def scrape_yahoo_finance(stock_symbol, max_headlines=10):
    """
    Python web scraper to scrape data from Yahoo Finance.

    param stock_symbol: String of a stock symbol to scrape data for.
    param max_headlines: Maximum number of headlines to scrape (default is 10).
    return: List of headlines from the respective Yahoo Finance website for the stock.
    """
    url = f"https://finance.yahoo.com/quote/{stock_symbol}/news"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            logging.error(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, "html.parser")
        headlines = []
        
        for item in soup.find_all("h3", limit=max_headlines):
            headline = item.text.strip()
            headlines.append(headline)
        
        if not headlines:
            logging.warning("No headlines found. The website structure might have changed.")
        
        return headlines
    
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while fetching data: {e}")
        return []

if __name__ == "__main__":
    stock_symbol = "AAPL"
    logging.info(f"Scraping news for stock: {stock_symbol}")
    news = scrape_yahoo_finance(stock_symbol)
    print(news)
    time.sleep(1)  # Respectful delay between requests
