"""
Tests for Portfolio Manager
"""

import unittest
from datetime import datetime
from src.portfolio import Portfolio, Position, PositionStatus

class TestPortfolio(unittest.TestCase):
    def setUp(self):
        self.portfolio = Portfolio(initial_capital=30000)
    
    def test_initial_capital(self):
        self.assertEqual(self.portfolio.initial_capital, 30000)
        self.assertEqual(self.portfolio.cash, 30000)
    
    def test_add_position(self):
        pos = self.portfolio.add_position(
            ticker="AAPL",
            position_type="CSP",
            strike=150.0,
            expiration="2026-03-21",
            contracts=1,
            premium=125.0
        )
        
        self.assertEqual(pos.ticker, "AAPL")
        self.assertEqual(pos.strike, 150.0)
        self.assertEqual(pos.premium_received, 125.0)
        self.assertEqual(pos.status, PositionStatus.OPEN)
        self.assertEqual(self.portfolio.cash, 30125.0)  # Premium added
    
    def test_position_capital_at_risk(self):
        pos = self.portfolio.add_position(
            ticker="AAPL",
            position_type="CSP",
            strike=150.0,
            expiration="2026-03-21",
            contracts=2,
            premium=250.0
        )
        
        # 2 contracts * $150 strike * 100 shares = $30,000
        self.assertEqual(pos.capital_at_risk, 30000.0)
    
    def test_close_position(self):
        pos = self.portfolio.add_position(
            ticker="AAPL",
            position_type="CSP",
            strike=150.0,
            expiration="2026-03-21",
            contracts=1,
            premium=125.0
        )
        
        closed = self.portfolio.close_position(pos.id, exit_price=0.50)
        
        self.assertIsNotNone(closed)
        self.assertEqual(closed.status, PositionStatus.CLOSED)
        # PnL = (1.25 - 0.50) * 100 = $75
        self.assertEqual(closed.pnl, 75.0)
        
        # Should be moved to history
        self.assertEqual(len(self.portfolio.get_open_positions()), 0)
        self.assertEqual(len(self.portfolio.trade_history), 1)
    
    def test_close_nonexistent_position(self):
        result = self.portfolio.close_position("FAKE_ID", exit_price=0.50)
        self.assertIsNone(result)
    
    def test_get_metrics_empty(self):
        metrics = self.portfolio.get_metrics()
        
        self.assertEqual(metrics['initial_capital'], 30000)
        self.assertEqual(metrics['current_cash'], 30000)
        self.assertEqual(metrics['total_trades'], 0)
        self.assertEqual(metrics['win_rate'], 0)
        self.assertEqual(metrics['total_pnl'], 0)
    
    def test_get_metrics_with_trades(self):
        # Add and close a winning trade
        pos1 = self.portfolio.add_position(
            ticker="AAPL",
            position_type="CSP",
            strike=150.0,
            expiration="2026-03-21",
            contracts=1,
            premium=150.0
        )
        self.portfolio.close_position(pos1.id, exit_price=0.50)  # $100 profit
        
        # Add and close a losing trade
        pos2 = self.portfolio.add_position(
            ticker="TSLA",
            position_type="CSP",
            strike=200.0,
            expiration="2026-03-21",
            contracts=1,
            premium=100.0
        )
        self.portfolio.close_position(pos2.id, exit_price=1.50)  # -$50 loss
        
        metrics = self.portfolio.get_metrics()
        
        self.assertEqual(metrics['total_trades'], 2)
        self.assertEqual(metrics['win_rate'], 0.5)  # 1 win, 1 loss
        self.assertEqual(metrics['total_pnl'], 50.0)  # $100 - $50

class TestPosition(unittest.TestCase):
    def test_days_held(self):
        pos = Position(
            id="TEST_001",
            ticker="AAPL",
            position_type="CSP",
            strike=150.0,
            expiration="2026-03-21",
            entry_date=datetime.now(),
            contracts=1,
            premium_received=125.0
        )
        
        # Days held should be 0 or 1
        self.assertGreaterEqual(pos.days_held, 0)
    
    def test_position_id_generation(self):
        portfolio = Portfolio()
        
        pos1 = portfolio.add_position("AAPL", "CSP", 150.0, "2026-03-21", 1, 125.0)
        pos2 = portfolio.add_position("TSLA", "CSP", 200.0, "2026-03-21", 1, 100.0)
        
        self.assertEqual(pos1.id, "TRADE_0001")
        self.assertEqual(pos2.id, "TRADE_0002")

if __name__ == "__main__":
    unittest.main()
