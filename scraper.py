import requests
from bs4 import BeautifulSoup


def scrape_yahoo_finance(stock_symbol):
    """
    Python web scraper to scrape data from Yahoo Finance
    
    param stock_symbol: String of a stock symbol to scrape data for
    return: array of headlines from the respective Yahoo finance website for the stock 
    """
    
    url = f"https://finance.yahoo.com/quote/{stock_symbol}/news"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    headlines = []
    for item in soup.find_all("h3"):
        headline = item.text.strip()
        headlines.append(headline)

    return headlines

if __name__ == "__main__":
    news = scrape_yahoo_finance("AAPL")
    print(news)
