import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict, List, Any
from src.base.base_agent import BaseAgent  # Absolute import path 

class QuantAnalyst(BaseAgent):
    def __init__(self, config_path: str):
        super().__init__("QuantAnalyst", config_path)
        self.config = self.config.get("quant_analysis", {})

    def analyze(self, strategy: str, tickers: list, timeframe: str) -> dict:
        """
        Perform quantitative analysis based on the strategy.
        """
        results = {}
        for ticker in tickers:
            ticker = ticker.strip().upper()  # Ensure ticker is a string and uppercase
            data = self.fetch_data(ticker, timeframe)
            if strategy == "mean_reversion":
                results[ticker] = self.mean_reversion_strategy(data)
            elif strategy == "momentum":
                results[ticker] = self.momentum_strategy(data)
            elif strategy == "pairs_trading":
                results[ticker] = self.pairs_trading_strategy(tickers)
            else:
                raise ValueError(f"Unknown strategy: {strategy}")
        return results

    def mean_reversion_strategy(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Mean reversion strategy: Identify if the stock is overbought or oversold.
        """
        if data.empty:
            raise ValueError("No data available for the given ticker.")

        rolling_mean = data["Close"].rolling(window=20).mean()
        rolling_std = data["Close"].rolling(window=20).std()

        z_score = (data["Close"] - rolling_mean) / rolling_std
        current_z_score = z_score.iloc[-1]

        return {
            "current_z_score": current_z_score,
            "rolling_mean": rolling_mean.iloc[-1],
            "rolling_std": rolling_std.iloc[-1],
        }

    def fetch_data(self, ticker: str, timeframe: str = "1y") -> pd.DataFrame:
        """ 
        Fetch historical data for the given ticker.
        """
        try:
            data = yf.Ticker(ticker).history(period=timeframe)
            if data.empty:
                raise ValueError(f"No data available for ticker: {ticker}")
            return data
        except Exception as e:
            raise ValueError(f"Failed to fetch data for {ticker}: {e}")
        
    def momentum_strategy(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Momentum strategy: Analyze momentum using rate of change or moving averages.
        """
        if data.empty:
            raise ValueError("No data available for the given ticker.")

        data["Momentum"] = data["Close"].diff(periods=10)
        momentum = data["Momentum"].iloc[-1]

        return {
            "momentum": momentum,
            "current_price": data["Close"].iloc[-1],
        }

    def pairs_trading_strategy(self, tickers: List[str]) -> Dict[str, Any]:
        """
        Pairs trading strategy: Analyze correlation and cointegration of two tickers.
        """
        if len(tickers) < 2:
            raise ValueError("Pairs trading requires at least two tickers.")
        
        data_1 = self.fetch_data(tickers[0])
        data_2 = self.fetch_data(tickers[1])

        if data_1.empty or data_2.empty:
            raise ValueError(f"No data available for tickers: {tickers}")

        prices_1 = data_1["Close"]
        prices_2 = data_2["Close"]

        correlation = prices_1.corr(prices_2)
        spread = prices_1 - prices_2

        return {
            "correlation": correlation,
            "mean_spread": spread.mean(),
            "std_spread": spread.std(),
        }

    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the Quant Analyst.
        """
        return {"config": self.config}
