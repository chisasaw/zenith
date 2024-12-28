from typing import NamedTuple 

class Signal(NamedTuple):
    ticker: str
    signal_type: str
    value: float
    timestamp: str

class SignalType:
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"
