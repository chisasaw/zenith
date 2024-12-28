# Zenith

Zenith is a comprehensive command-line tool designed to perform advanced market analysis, sentiment analysis, quantitative analysis, and portfolio management. The project leverages data-driven insights to empower users in making informed financial decisions. This version is 0.1.0 and essential for educational purposes only. 

## Features

### Market Data Analyst
- Analyze key metrics like moving averages, RSI, and volatility for selected stock tickers.
- Provides in-depth technical analysis.

### Sentiment Analyst
- Tracks Google Trends data for specified keywords.
- Visualizes trends to provide actionable sentiment insights.

### Quantitative Analyst
- Implements various trading strategies, including:
  - Momentum
  - Mean Reversion
  - Pairs Trading

### Portfolio Manager Analyst
- Manages and analyzes portfolio performance.
- Visualizes portfolio performance metrics and correlation matrix.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/chisasaw/zenith.git
   cd zenith
   ```

2. Set up a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Zenith's functionality is divided into four main agents: Market Data Analyst, Sentiment Analyst, Quantitative Analyst, and Portfolio Manager Analyst.

### Market Data Analyst
```bash
python -m src.terminal.cli market-analysis --tickers "AAPL,MSFT" --config-path "config/market_analyst_config.yaml"
```

### Sentiment Analyst
```bash
python -m src.terminal.cli sentiment-analysis --keywords "Apple,Microsoft" --timeframe "now 7-d" --region "US" --config-path "config/market_analyst_config.yaml"
```

### Quantitative Analyst
- Momentum Strategy:
  ```bash
  python -m src.terminal.cli quant-analysis --strategy "momentum" --tickers "AAPL,MSFT" --timeframe "1y" --config-path "config/market_analyst_config.yaml"
  ```

- Mean Reversion Strategy:
  ```bash
  python -m src.terminal.cli quant-analysis --strategy "mean_reversion" --tickers "AAPL,MSFT" --timeframe "1y" --config-path "config/market_analyst_config.yaml"
  ```

- Pairs Trading Strategy:
  ```bash
  python -m src.terminal.cli quant-analysis --strategy "pairs_trading" --tickers "AAPL,MSFT" --timeframe "1y" --config-path "config/market_analyst_config.yaml"
  ```

### Portfolio Manager Analyst
```bash
python -m src.terminal.cli portfolio-manager --portfolio '{"AAPL": 0.4, "MSFT": 0.6}' --timeframe "1y" --config-path "config/market_analyst_config.yaml"
```

---

## Configuration

Zenith requires a configuration file for the Market Data Analyst. An example configuration file is provided in the `config` directory:
- `market_analyst_config.yaml`

Update this file with your API keys and preferences.

---

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests.

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-branch
   ```
5. Submit a pull request.

---

## Author

**Warren Chisasa**  
GitHub: [@chisasaw](https://github.com/chisasaw)

---

## License

MIT License 

Copyright (c) 2024 Warren Chisasa

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

