# src/models/trading_signals.py 
from enum import Enum

class SignalType(Enum):
    MA_CROSSOVER_BULLISH = "ma_crossover_bullish"
    MA_CROSSOVER_BEARISH = "ma_crossover_bearish"
    RSI_OVERSOLD = "rsi_oversold"
    RSI_OVERBOUGHT = "rsi_overbought"
    HIGH_VOLATILITY = "high_volatility"

# src/models/data_models.py
from typing import Dict, Any
import pandas as pd  # Ensure pandas is properly imported

class Signal:
    def __init__(self, signal_type: str, data: Dict[str, Any]):
        self.signal_type = signal_type
        self.data = data
        self.timestamp = pd.Timestamp.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.signal_type,
            "data": self.data,
            "timestamp": self.timestamp
        }
