"""
Unit tests for CSP Scanner
"""

import unittest
from datetime import datetime
from src.scanner import CSPScanner, CSPParameters, OptionContract, TradeOpportunity, TradeStatus

class TestCSPParameters(unittest.TestCase):
    def test_default_params(self):
        params = CSPParameters()
        self.assertEqual(params.min_otm_percent, 10.0)
        self.assertEqual(params.max_otm_percent, 15.0)
        self.assertEqual(params.min_delta, 0.20)
        self.assertEqual(params.max_delta, 0.35)
        self.assertEqual(params.min_weekly_yield, 0.007)

class TestOptionContract(unittest.TestCase):
    def test_mid_price_calculation(self):
        contract = OptionContract(
            symbol="AAPL240315P00150000",
            strike=150.0,
            expiration="2024-03-15",
            bid=1.50,
            ask=1.70,
            delta=-0.25,
            gamma=0.02,
            theta=-0.05,
            vega=0.10,
            iv=0.30,
            open_interest=500,
            volume=100
        )
        self.assertEqual(contract.mid_price, 1.60)
    
    def test_spread_percent(self):
        contract = OptionContract(
            symbol="AAPL240315P00150000",
            strike=150.0,
            expiration="2024-03-15",
            bid=1.50,
            ask=1.70,
            delta=-0.25,
            gamma=0.02,
            theta=-0.05,
            vega=0.10,
            iv=0.30,
            open_interest=500,
            volume=100
        )
        expected_spread = (1.70 - 1.50) / 1.60
        self.assertAlmostEqual(contract.spread_percent, expected_spread)

class TestTradeEvaluation(unittest.TestCase):
    def setUp(self):
        self.scanner = CSPScanner("fake_token", "fake_token")
    
    def test_qualified_trade(self):
        """Test a trade that meets all criteria"""
        contract = OptionContract(
            symbol="AAPL240315P00150000",
            strike=150.0,
            expiration="2024-03-15",
            bid=1.50,
            ask=1.70,
            delta=-0.25,  # Within 0.20-0.35
            gamma=0.02,
            theta=-0.05,
            vega=0.10,
            iv=0.30,
            open_interest=500,  # > 200
            volume=100
        )
        
        current_price = 170.0  # 11.8% OTM (within 10-15%)
        
        opp = self.scanner.evaluate_contract("AAPL", current_price, contract)
        
        # Check OTM percent
        expected_otm = ((170 - 150) / 170) * 100
        self.assertAlmostEqual(opp.otm_percent, expected_otm, places=1)
        
        # This should be qualified
        self.assertEqual(opp.status, TradeStatus.QUALIFIED)
        self.assertIsNone(opp.rejection_reason)
    
    def test_rejected_low_delta(self):
        """Test rejection due to low delta"""
        contract = OptionContract(
            symbol="AAPL240315P00150000",
            strike=150.0,
            expiration="2024-03-15",
            bid=1.50,
            ask=1.70,
            delta=-0.10,  # Too low
            gamma=0.02,
            theta=-0.05,
            vega=0.10,
            iv=0.30,
            open_interest=500,
            volume=100
        )
        
        opp = self.scanner.evaluate_contract("AAPL", 170.0, contract)
        self.assertEqual(opp.status, TradeStatus.REJECTED)
        self.assertIn("Delta", opp.rejection_reason)
    
    def test_rejected_high_delta(self):
        """Test rejection due to high delta"""
        contract = OptionContract(
            symbol="AAPL240315P00150000",
            strike=150.0,
            expiration="2024-03-15",
            bid=1.50,
            ask=1.70,
            delta=-0.40,  # Too high
            gamma=0.02,
            theta=-0.05,
            vega=0.10,
            iv=0.30,
            open_interest=500,
            volume=100
        )
        
        opp = self.scanner.evaluate_contract("AAPL", 170.0, contract)
        self.assertEqual(opp.status, TradeStatus.REJECTED)
        self.assertIn("Delta", opp.rejection_reason)
    
    def test_rejected_low_otm(self):
        """Test rejection due to insufficient OTM buffer"""
        contract = OptionContract(
            symbol="AAPL240315P00150000",
            strike=165.0,  # Only 3% OTM
            expiration="2024-03-15",
            bid=1.50,
            ask=1.70,
            delta=-0.25,
            gamma=0.02,
            theta=-0.05,
            vega=0.10,
            iv=0.30,
            open_interest=500,
            volume=100
        )
        
        opp = self.scanner.evaluate_contract("AAPL", 170.0, contract)
        self.assertEqual(opp.status, TradeStatus.REJECTED)
        self.assertIn("OTM", opp.rejection_reason)
    
    def test_rejected_low_open_interest(self):
        """Test rejection due to low liquidity"""
        contract = OptionContract(
            symbol="AAPL240315P00150000",
            strike=150.0,
            expiration="2024-03-15",
            bid=1.50,
            ask=1.70,
            delta=-0.25,
            gamma=0.02,
            theta=-0.05,
            vega=0.10,
            iv=0.30,
            open_interest=50,  # Too low
            volume=100
        )
        
        opp = self.scanner.evaluate_contract("AAPL", 170.0, contract)
        self.assertEqual(opp.status, TradeStatus.REJECTED)
        self.assertIn("OI", opp.rejection_reason)

class TestYieldCalculations(unittest.TestCase):
    def setUp(self):
        self.scanner = CSPScanner("fake_token", "fake_token")
    
    def test_weekly_yield_calculation(self):
        contract = OptionContract(
            symbol="AAPL240315P00150000",
            strike=150.0,
            expiration="2024-03-15",
            bid=1.00,
            ask=1.00,  # $1.00 mid
            delta=-0.25,
            gamma=0.02,
            theta=-0.05,
            vega=0.10,
            iv=0.30,
            open_interest=500,
            volume=100
        )
        
        opp = self.scanner.evaluate_contract("AAPL", 170.0, contract)
        
        # Premium = $1.00 * 100 = $100
        # Capital at risk = $150 * 100 = $15,000
        # Raw return = $100 / $15,000 = 0.67%
        # Weekly = 0.67% / (10/7) ≈ 0.47%
        
        self.assertLess(opp.weekly_yield, 0.007)  # Should be rejected for low yield

if __name__ == "__main__":
    unittest.main()
