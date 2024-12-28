import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict
from src.base.base_agent import BaseAgent  # Absolute import path
from src.models.trading_signals import SignalType  # Absolute import path
from src.models.data_models import Signal  # Absolute import path 

class MarketDataAnalyst(BaseAgent):
    def __init__(self, config_path: str):
        super().__init__("MarketDataAnalyst", config_path)

        # Load configuration for analysis
        self.analysis_config = self.config.get("analysis", {})
        self.moving_averages: Dict[str, Dict[str, float]] = {}
        self.rsi_values: Dict[str, float] = {}
        self.volatility: Dict[str, float] = {}

    def analyze_moving_averages(self, ticker: str, short_window: int = 20, long_window: int = 50) -> Dict[str, float]:
        """Calculate and return moving averages for a ticker."""
        data = self._fetch_ticker_data(ticker)
        if data.empty:
            raise ValueError(f"No data available for ticker: {ticker}")

        short_ma = data["Close"].rolling(window=short_window).mean().iloc[-1]
        long_ma = data["Close"].rolling(window=long_window).mean().iloc[-1]

        self.moving_averages[ticker] = {"short": short_ma, "long": long_ma}

        return {"short": short_ma, "long": long_ma}

    def analyze_rsi(self, ticker: str, period: int = 14) -> float:
        """Calculate and return the RSI for a ticker."""
        data = self._fetch_ticker_data(ticker)
        if data.empty:
            raise ValueError(f"No data available for ticker: {ticker}")

        delta = data["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        rsi_value = rsi.iloc[-1]

        self.rsi_values[ticker] = rsi_value

        return rsi_value

    def analyze_volatility(self, ticker: str, period: int = 20) -> float:
        """Calculate and return the volatility for a ticker."""
        data = self._fetch_ticker_data(ticker)
        if data.empty:
            raise ValueError(f"No data available for ticker: {ticker}")

        returns = np.log(data["Close"] / data["Close"].shift(1))
        volatility = returns.rolling(window=period).std() * np.sqrt(252)  # Annualized volatility
        volatility_value = volatility.iloc[-1]

        self.volatility[ticker] = volatility_value

        return volatility_value

    def _fetch_ticker_data(self, ticker: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        """Fetch historical market data for a ticker."""
        ticker_data = yf.Ticker(ticker).history(period=period, interval=interval)
        if ticker_data.empty:
            raise ValueError(f"Failed to fetch data for ticker: {ticker}")
        return ticker_data

    def get_status(self) -> Dict[str, Dict[str, float]]:
        """Get the current analysis status."""
        return {
            "moving_averages": self.moving_averages,
            "rsi_values": self.rsi_values,
            "volatility": self.volatility,
        }

    