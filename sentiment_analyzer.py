#!/usr/bin/env python3
# filepath: /Users/saathvik/projects/AIStockSentiment/sentiment_analyzer.py

import logging
from scraper import scrape_yahoo_finance
import pandas as pd
from transformers import pipeline
import time
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class SentimentAnalyzer:
    """
    Class to analyze sentiment of headlines scraped from Yahoo Finance.
    Uses Hugging Face's transformers library for sentiment analysis.
    """
    def __init__(self):
        # Initialize the sentiment analysis pipeline
        try:
            self.sentiment_analyzer = pipeline("sentiment-analysis")
            logging.info("Sentiment analysis pipeline initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize sentiment analysis pipeline: {e}")
            raise

    def analyze_headlines(self, headlines):
        """
        Analyze the sentiment of a list of headlines.
        
        param headlines: List of headlines to analyze
        return: DataFrame with headlines and their sentiment scores
        """
        if not headlines:
            logging.warning("No headlines to analyze")
            return pd.DataFrame(columns=["headline", "sentiment", "score"])
        
        results = []
        for headline in headlines:
            try:
                # Get sentiment prediction
                sentiment_result = self.sentiment_analyzer(headline)[0]
                sentiment = sentiment_result["label"]
                score = sentiment_result["score"]
                
                # Normalize sentiment labels
                if sentiment.lower() == "positive" or sentiment.lower() == "pos":
                    normalized_sentiment = "positive"
                elif sentiment.lower() == "negative" or sentiment.lower() == "neg":
                    normalized_sentiment = "negative"
                else:
                    normalized_sentiment = "neutral"
                
                results.append({
                    "headline": headline,
                    "sentiment": normalized_sentiment,
                    "score": score
                })
                
            except Exception as e:
                logging.error(f"Error analyzing headline: {headline}. Error: {e}")
        
        return pd.DataFrame(results)
    
    def get_overall_sentiment(self, sentiment_df):
        """
        Calculate the overall sentiment score based on the analyzed headlines.
        
        param sentiment_df: DataFrame with sentiment analysis results
        return: Dict with overall sentiment stats
        """
        if sentiment_df.empty:
            return {"overall": "neutral", "score": 0.5}
        
        # Count sentiments
        sentiment_counts = sentiment_df["sentiment"].value_counts().to_dict()
        
        # Calculate average scores
        avg_score = sentiment_df["score"].mean()
        
        # Determine overall sentiment
        pos_count = sentiment_counts.get("positive", 0)
        neg_count = sentiment_counts.get("negative", 0)
        
        if pos_count > neg_count:
            overall = "positive"
        elif neg_count > pos_count:
            overall = "negative"
        else:
            overall = "neutral"
        
        return {
            "overall": overall,
            "score": avg_score,
            "counts": sentiment_counts
        }
    
    def visualize_sentiment(self, sentiment_df, stock_symbol):
        """
        Create a simple visualization of sentiment analysis results.
        
        param sentiment_df: DataFrame with sentiment analysis results
        param stock_symbol: Stock symbol for which sentiment is analyzed
        """
        if sentiment_df.empty:
            logging.warning("No data to visualize")
            return
        
        # Count sentiments
        sentiment_counts = sentiment_df["sentiment"].value_counts()
        
        # Create bar chart
        plt.figure(figsize=(10, 6))
        colors = {'positive': 'green', 'negative': 'red', 'neutral': 'gray'}
        sentiment_counts.plot(kind='bar', color=[colors.get(x, 'blue') for x in sentiment_counts.index])
        plt.title(f'Sentiment Analysis for {stock_symbol} Headlines')
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        plt.tight_layout()
        
        # Save the chart
        plt.savefig(f"{stock_symbol}_sentiment.png")
        logging.info(f"Sentiment visualization saved as {stock_symbol}_sentiment.png")
        
        # Show the chart
        plt.show()


def analyze_stock_sentiment(stock_symbol, max_headlines=20):
    """
    Main function to scrape headlines and analyze sentiment for a given stock.
    
    param stock_symbol: Stock symbol to analyze
    param max_headlines: Maximum number of headlines to scrape
    return: Tuple of (DataFrame with sentiment analysis, overall sentiment dict)
    """
    # Scrape headlines
    logging.info(f"Scraping headlines for {stock_symbol}")
    headlines = scrape_yahoo_finance(stock_symbol, max_headlines)
    
    if not headlines:
        logging.warning(f"No headlines found for {stock_symbol}")
        return pd.DataFrame(), {"overall": "neutral", "score": 0.5}
    
    # Analyze sentiment
    logging.info(f"Analyzing sentiment for {len(headlines)} headlines")
    analyzer = SentimentAnalyzer()
    sentiment_df = analyzer.analyze_headlines(headlines)
    
    # Get overall sentiment
    overall_sentiment = analyzer.get_overall_sentiment(sentiment_df)
    logging.info(f"Overall sentiment for {stock_symbol}: {overall_sentiment['overall']} (Score: {overall_sentiment['score']:.2f})")
    
    return sentiment_df, overall_sentiment


if __name__ == "__main__":
    stock_symbol = "AAPL"
    
    logging.info(f"Starting sentiment analysis for {stock_symbol}")
    start_time = time.time()
    
    sentiment_df, overall_sentiment = analyze_stock_sentiment(stock_symbol)
    
    # Print results
    print(f"\nSentiment Analysis Results for {stock_symbol}:")
    print(f"Overall Sentiment: {overall_sentiment['overall']}")
    print(f"Average Score: {overall_sentiment['score']:.2f}")
    
    if 'counts' in overall_sentiment:
        print("\nSentiment Distribution:")
        for sentiment, count in overall_sentiment['counts'].items():
            print(f"  {sentiment.capitalize()}: {count}")
    
    print("\nHeadline Sentiment Details:")
    if not sentiment_df.empty:
        pd.set_option('display.max_colwidth', None)
        print(sentiment_df[["headline", "sentiment", "score"]])
        
        # Create visualization
        analyzer = SentimentAnalyzer()
        analyzer.visualize_sentiment(sentiment_df, stock_symbol)
    
    elapsed_time = time.time() - start_time
    logging.info(f"Sentiment analysis completed in {elapsed_time:.2f} seconds")
