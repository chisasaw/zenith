import numpy as np
import pandas as pd
import yfinance as yf
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import seaborn as sns 

class PortfolioManagerAnalyst:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.portfolio: Dict[str, float] = {}  # {ticker: weight}
        self.historical_data: Dict[str, pd.DataFrame] = {}
        self.timeframe = "1y"

    def set_portfolio(self, portfolio: Dict[str, float]):
        """
        Set portfolio with tickers and their respective weights.
        """
        if not portfolio or not isinstance(portfolio, dict):
            raise ValueError("Portfolio must be a non-empty dictionary with {ticker: weight} format.")
        if not np.isclose(sum(portfolio.values()), 1):
            raise ValueError("Portfolio weights must sum up to 1.")
        self.portfolio = portfolio

    def fetch_data(self):
        """
        Fetch historical price data for all portfolio tickers.
        """
        for ticker in self.portfolio.keys():
            data = yf.Ticker(ticker).history(period=self.timeframe)
            if data.empty:
                raise ValueError(f"No data found for ticker: {ticker}")
            self.historical_data[ticker] = data["Close"]

    def calculate_portfolio_metrics(self) -> Dict[str, Any]:
        """
        Calculate portfolio metrics like returns, volatility, and Sharpe ratio.
        """
        if not self.historical_data:
            raise ValueError("Historical data is empty. Fetch data first.")

        returns = pd.DataFrame(self.historical_data).pct_change().dropna()
        weights = np.array(list(self.portfolio.values()))
        mean_returns = returns.mean()
        cov_matrix = returns.cov()

        portfolio_return = np.dot(weights, mean_returns)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = portfolio_return / portfolio_volatility if portfolio_volatility != 0 else np.nan

        return {
            "portfolio_return": portfolio_return,
            "portfolio_volatility": portfolio_volatility,
            "sharpe_ratio": sharpe_ratio,
        }

    def visualize_portfolio_performance(self):
        """
        Visualize portfolio performance.
        """
        if not self.historical_data:
            raise ValueError("Historical data is empty. Fetch data first.")

        portfolio_values = pd.DataFrame(self.historical_data).dot(list(self.portfolio.values()))
        normalized_values = portfolio_values / portfolio_values.iloc[0]  # Normalize to start at 1.0

        plt.figure(figsize=(10, 6))
        plt.plot(normalized_values, label="Portfolio")
        plt.title("Portfolio Performance")
        plt.xlabel("Date")
        plt.ylabel("Normalized Value")
        plt.legend()
        plt.grid()
        plt.show()

    def visualize_correlation_matrix(self):
        """
        Visualize the correlation matrix of the portfolio's assets.
        """
        if not self.historical_data:
            raise ValueError("Historical data is empty. Fetch data first.")

        returns = pd.DataFrame(self.historical_data).pct_change().dropna()
        correlation_matrix = returns.corr()

        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Matrix")
        plt.show()

    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the Portfolio Manager Analyst.
        """
        return {
            "portfolio": self.portfolio,
            "timeframe": self.timeframe,
        }
