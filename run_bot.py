#!/usr/bin/env python3
"""
Kelvin Capital - Main Trading Bot

Runs the complete CSP scanning and trading workflow.
"""

import os
import sys
from typing import List

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.scanner import CSPScanner
from src.portfolio import Portfolio
from src.earnings import EarningsCalendar
from src.config import ConfigManager
from src.utils import setup_logger, format_currency, format_percent, Colors

# 51 tickers from S&P 500
UNIVERSE = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "NVDA", "JPM", "JNJ", "V",
    "UNH", "HD", "PG", "MA", "BAC", "ABBV", "PFE", "KO", "PEP", "COST",
    "TMO", "AVGO", "DIS", "WMT", "CSCO", "VZ", "ADBE", "CRM", "ACN", "WFC",
    "MRK", "NKE", "ABT", "CMCSA", "XOM", "TXN", "QCOM", "NEE", "PM", "RTX",
    "HON", "BMY", "UNP", "LIN", "LOW", "AMGN", "UPS", "T", "CVX", "SBUX"
]

logger = setup_logger("kelvin")

def main():
    """Main trading bot entry point"""
    logger.info("="*60)
    logger.info("KELVIN CAPITAL TRADING BOT")
    logger.info("="*60)
    
    # Load configuration
    config = ConfigManager()
    config.load_from_env()
    
    if not config.validate():
        logger.error("Missing required API keys. Set TRADIER_TOKEN and FINNHUB_TOKEN.")
        sys.exit(1)
    
    logger.info("Configuration loaded successfully")
    
    # Initialize components
    scanner = CSPScanner(
        tradier_token=config.get_api_key('tradier'),
        finnhub_token=config.get_api_key('finnhub')
    )
    
    portfolio = Portfolio(initial_capital=config.trading_config.initial_capital)
    earnings = EarningsCalendar(config.get_api_key('finnhub'))
    
    logger.info(f"Portfolio initialized: {format_currency(portfolio.initial_capital)}")
    
    # Run scan
    logger.info(f"Scanning {len(UNIVERSE)} tickers...")
    opportunities = scanner.scan_universe(UNIVERSE[:10])  # Limit for testing
    
    # Filter out earnings risks
    safe_opportunities = []
    for opp in opportunities:
        if earnings.is_safe_to_trade(opp.ticker, days_buffer=7):
            safe_opportunities.append(opp)
        else:
            logger.warning(f"Skipping {opp.ticker} - earnings too close")
    
    # Display results
    logger.info("="*60)
    logger.info("SCAN RESULTS")
    logger.info("="*60)
    
    if not safe_opportunities:
        logger.info("No qualifying trades found.")
        return
    
    for opp in safe_opportunities[:5]:
        print(f"\n{Colors.colorize(opp.ticker, Colors.GREEN)} ${opp.contract.strike} Put")
        print(f"  Expiration: {opp.contract.expiration}")
        print(f"  Premium: {format_currency(opp.contract.mid_price)}")
        print(f"  Delta: {abs(opp.contract.delta):.2f}")
        print(f"  OTM Buffer: {format_percent(opp.otm_percent/100)}")
        print(f"  Weekly Yield: {format_percent(opp.weekly_yield)}")
        print(f"  Annualized: {format_percent(opp.annualized_yield)}")
    
    # Portfolio metrics
    metrics = portfolio.get_metrics()
    logger.info("="*60)
    logger.info("PORTFOLIO STATUS")
    logger.info("="*60)
    logger.info(f"Cash: {format_currency(metrics['current_cash'])}")
    logger.info(f"Open Positions: {metrics['open_positions']}")
    logger.info(f"Total Trades: {metrics['total_trades']}")
    logger.info(f"Win Rate: {format_percent(metrics['win_rate'])}")
    logger.info(f"Total P&L: {format_currency(metrics['total_pnl'])}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nBot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
