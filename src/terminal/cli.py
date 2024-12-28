import click
from src.agents.market_analyst import MarketDataAnalyst
from src.agents.sentiment_analyst import SentimentAnalyst
from src.agents.quant_analyst import QuantAnalyst 
from src.agents.portfolio_manager_analyst import PortfolioManagerAnalyst 
from src.core.logger import setup_logging
import json

# Initialize logging 
logger = setup_logging()

@click.group()
def cli():
    """CLI for Zenith AI Tools"""
    pass

# Market Analysis Command
@cli.command(name="market-analysis")
@click.option(
    "--tickers",
    prompt="Enter tickers (comma-separated)",
    help="Comma-separated list of tickers to analyze",
)
@click.option(
    "--config-path",
    default="config/market_analyst_config.yaml",
    help="Path to configuration file",
)
def market_analysis(tickers, config_path):
    """
    Perform market analysis for the provided tickers.
    """
    tickers_list = [ticker.strip() for ticker in tickers.split(",")]
    try:
        market_analyst = MarketDataAnalyst(config_path)
        for ticker in tickers_list:
            logger.info(f"Analyzing market data for {ticker}")
            moving_averages = market_analyst.analyze_moving_averages(ticker)
            rsi = market_analyst.analyze_rsi(ticker)
            volatility = market_analyst.analyze_volatility(ticker)

            click.echo(f"\nMarket Analysis for {ticker}:")
            click.echo(f"Moving Averages: {moving_averages}")
            click.echo(f"RSI: {rsi}")
            click.echo(f"Volatility: {volatility}")
    except Exception as e:
        logger.error(f"Error analyzing market data: {e}")
        click.echo(f"Error: {e}")

# Sentiment Analysis Command
@cli.command(name="sentiment-analysis")
@click.option(
    "--keywords",
    prompt="Enter keywords (comma-separated)",
    help="Comma-separated list of keywords to analyze sentiment",
)
@click.option("--timeframe", default="now 7-d", help="Timeframe for trends (default: now 7-d)")
@click.option("--region", default="US", help="Region for trends (default: US)")
@click.option(
    "--config-path",
    default="config/sentiment_analyst_config.yaml",
    help="Path to configuration file",
)
def sentiment_analysis(keywords, timeframe, region, config_path):
    """
    Perform sentiment analysis for the provided keywords.
    """
    keywords_list = [kw.strip() for kw in keywords.split(",")]
    try:
        sentiment_analyst = SentimentAnalyst(config_path)
        # Get trending keywords and visualize the trends
        trends = sentiment_analyst.get_trending_keywords(keywords_list, timeframe, region)
        sentiment_analyst.visualize_trends(trends)

        click.echo("\nSentiment Analysis Complete.")
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {e}")
        click.echo(f"Error: {e}")

# Quantitative Analysis Command
@cli.command(name="quant-analysis")
@click.option(
    "--strategy",
    prompt="Enter strategy (mean_reversion, momentum, pairs_trading)",
    help="The strategy to analyze",
)
@click.option(
    "--tickers",
    prompt="Enter tickers (comma-separated)",
    help="Comma-separated list of tickers to analyze",
)
@click.option(
    "--timeframe",
    default="1y",
    help="Timeframe for analysis (e.g., 1mo, 6mo, 1y)",
)
@click.option(
    "--config-path",
    default="config/quant_analyst_config.yaml",
    help="Path to configuration file",
)
@click.option(
    "--output",
    default=None,
    help="Optional path to save results as a JSON file",
)
def quant_analysis(strategy, tickers, timeframe, config_path, output):
    """
    Perform quantitative analysis using the specified strategy.
    """
    tickers_list = [ticker.strip() for ticker in tickers.split(",")]
    try:
        quant_analyst = QuantAnalyst(config_path=config_path)
        results = quant_analyst.analyze(strategy=strategy, tickers=tickers_list, timeframe=timeframe)

        click.echo("Quantitative Analysis Results:")
        click.echo(json.dumps(results, indent=4))

        if output:
            with open(output, "w") as file:
                json.dump(results, file, indent=4)
            click.echo(f"Results saved to {output}")
    except AttributeError as e:
        logger.error(f"Method error in QuantAnalyst: {e}")
        click.echo(f"Error: {e}")
    except Exception as e:
        logger.error(f"Error performing quantitative analysis: {e}")
        click.echo(f"Error: {e}")


# Portfolio Manager Command 
@cli.command(name="portfolio-manager")
@click.option("--portfolio", required=True, help="Portfolio in JSON format, e.g., '{\"AAPL\": 0.4, \"GOOGL\": 0.3, \"MSFT\": 0.3}'")
@click.option("--timeframe", default="1y", help="Timeframe for historical data.")
@click.option("--config-path", required=True, help="Path to config file.")
def portfolio_manager(portfolio, timeframe, config_path):
    """
    Manage portfolio, analyze performance, and visualize metrics.
    """
    try:
        portfolio = json.loads(portfolio)
        manager = PortfolioManagerAnalyst(config_path)
        manager.set_portfolio(portfolio)
        manager.timeframe = timeframe
        manager.fetch_data()
        
        metrics = manager.calculate_portfolio_metrics()
        click.echo(f"Portfolio Metrics: {metrics}")

        click.echo("Visualizing portfolio performance...")
        manager.visualize_portfolio_performance()

        click.echo("Visualizing correlation matrix...")
        manager.visualize_correlation_matrix()

    except Exception as e:
        click.echo(f"Error: {e}")



if __name__ == "__main__":
    cli()
