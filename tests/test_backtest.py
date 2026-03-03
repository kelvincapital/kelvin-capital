"""
Tests for Backtesting Engine
"""

import unittest
from datetime import datetime
from src.backtester import Backtester, HistoricalTrade

class TestBacktester(unittest.TestCase):
    def setUp(self):
        self.backtester = Backtester(initial_capital=30000)
    
    def test_initial_capital(self):
        self.assertEqual(self.backtester.initial_capital, 30000)
        self.assertEqual(self.backtester.cash, 30000)
    
    def test_simulate_trade(self):
        trade = self.backtester.simulate_trade(
            ticker="AAPL",
            entry_date=datetime(2023, 1, 1),
            stock_price=150.0,
            strike=135.0,
            premium=1.50,
            days_to_expiry=14
        )
        
        self.assertEqual(trade.ticker, "AAPL")
        self.assertEqual(trade.strike, 135.0)
        self.assertEqual(trade.premium, 1.50)
        self.assertIsNotNone(trade.pnl)
        
        # Should have one trade in history
        self.assertEqual(len(self.backtester.trades), 1)
    
    def test_multiple_trades(self):
        for i in range(10):
            self.backtester.simulate_trade(
                ticker="AAPL",
                entry_date=datetime(2023, 1, 1),
                stock_price=150.0,
                strike=135.0,
                premium=1.50,
                days_to_expiry=14
            )
        
        self.assertEqual(len(self.backtester.trades), 10)
        
        metrics = self.backtester.get_metrics()
        self.assertEqual(metrics['total_trades'], 10)
    
    def test_metrics_calculation(self):
        # Add some trades with known outcomes
        trade1 = HistoricalTrade(
            ticker="AAPL", entry_date=datetime(2023, 1, 1),
            exit_date=datetime(2023, 1, 15),
            strike=150.0, premium=1.50,
            exit_price=1.50, assigned=False, pnl=150.0
        )
        trade2 = HistoricalTrade(
            ticker="TSLA", entry_date=datetime(2023, 1, 1),
            exit_date=datetime(2023, 1, 15),
            strike=200.0, premium=2.00,
            exit_price=1.00, assigned=True, pnl=100.0
        )
        
        self.backtester.trades = [trade1, trade2]
        
        metrics = self.backtester.get_metrics()
        self.assertEqual(metrics['total_trades'], 2)
        self.assertEqual(metrics['total_pnl'], 250.0)
        self.assertEqual(metrics['win_rate'], 1.0)  # Both profitable
    
    def test_run_backtest(self):
        tickers = ["AAPL", "MSFT", "GOOGL"]
        start = datetime(2023, 1, 1)
        end = datetime(2023, 3, 31)
        
        metrics = self.backtester.run_backtest(tickers, start, end, trades_per_month=2)
        
        self.assertGreater(metrics['total_trades'], 0)
        self.assertIn('win_rate', metrics)
        self.assertIn('sharpe_ratio', metrics)
        self.assertIn('max_drawdown', metrics)

if __name__ == "__main__":
    unittest.main()
