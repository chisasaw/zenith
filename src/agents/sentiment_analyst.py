import matplotlib.pyplot as plt
from pytrends.request import TrendReq
from typing import Dict, List, Any
import pandas as pd # Ensure pandas is properly imported 

class SentimentAnalyst:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.pytrends = TrendReq(hl="en-US", tz=360)
        self.trending_keywords: List[str] = []

    def get_trending_keywords(self, keywords: List[str], timeframe: str = "now 7-d", region: str = "") -> Dict[str, Any]:
        """
        Fetch interest trends for given keywords using Google Trends.
        """
        if not keywords:
            raise ValueError("Keywords list is empty.")
        
        self.pytrends.build_payload(keywords, timeframe=timeframe, geo=region)
        data = self.pytrends.interest_over_time()

        if data.empty:
            raise ValueError("No data found for the given keywords.")
        
        # Extract the trend data
        trends = {keyword: data[keyword].tolist() for keyword in keywords}
        self.trending_keywords = trends
        
        # Visualize the trends using matplotlib
        self.visualize_trends(data, keywords)

        return trends

    def get_related_queries(self, keyword: str) -> Dict[str, Any]:
        """
        Fetch related queries for a given keyword.
        """
        self.pytrends.build_payload([keyword])
        queries = self.pytrends.related_queries()
        return queries.get(keyword, {})

    def visualize_trends(self, data: pd.DataFrame, keywords: List[str]):
        """
        Visualize the trends of the keywords over time.
        """
        plt.figure(figsize=(10, 6))
        
        # Plotting each keyword's trend
        for keyword in keywords:
            plt.plot(data.index, data[keyword], label=keyword)

        plt.title("Google Trends for Keywords")
        plt.xlabel("Date")
        plt.ylabel("Interest over time")
        plt.legend(title="Keywords")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Show the plot
        plt.show()
