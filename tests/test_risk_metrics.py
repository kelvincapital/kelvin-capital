"""
Tests for Risk Metrics Calculator
"""

import unittest
from src.risk_metrics import RiskCalculator

class TestRiskCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = RiskCalculator()
    
    def test_calculate_var(self):
        returns = [0.01, -0.02, 0.015, -0.01, 0.005, -0.005, 0.02, -0.015, 0.01, 0.005]
        capital = 10000
        
        var = self.calc.calculate_var(returns, capital)
        
        self.assertIn('var_95', var)
        self.assertIn('var_99', var)
        self.assertIn('expected_shortfall', var)
        
        # VaR should be positive
        self.assertGreater(var['var_95'], 0)
        self.assertGreater(var['var_99'], 0)
        
        # 99% VaR should be >= 95% VaR
        self.assertGreaterEqual(var['var_99'], var['var_95'])
    
    def test_calculate_var_empty(self):
        var = self.calc.calculate_var([], 10000)
        self.assertEqual(var['var_95'], 0)
        self.assertEqual(var['var_99'], 0)
    
    def test_sharpe_ratio(self):
        # Consistent positive returns
        returns = [0.001] * 10
        sharpe = self.calc.calculate_sharpe_ratio(returns)
        
        # Sharpe should be high for consistent returns
        self.assertGreater(sharpe, 0)
    
    def test_sharpe_ratio_empty(self):
        sharpe = self.calc.calculate_sharpe_ratio([])
        self.assertEqual(sharpe, 0.0)
    
    def test_sortino_ratio(self):
        # Mostly positive, some negative
        returns = [0.01, 0.02, -0.01, 0.015, 0.005, -0.005]
        sortino = self.calc.calculate_sortino_ratio(returns)
        
        self.assertGreater(sortino, 0)
    
    def test_sortino_no_downside(self):
        # All positive returns
        returns = [0.01, 0.02, 0.015, 0.005]
        sortino = self.calc.calculate_sortino_ratio(returns)
        
        # Should be infinity with no downside
        self.assertEqual(sortino, float('inf'))
    
    def test_max_drawdown(self):
        equity = [100, 110, 105, 120, 115, 100, 125, 120]
        
        dd = self.calc.calculate_max_drawdown(equity)
        
        # Max drawdown from 120 to 100 = 16.67%
        self.assertGreater(dd, 0)
        self.assertLess(dd, 0.20)
    
    def test_max_drawdown_no_drawdown(self):
        equity = [100, 110, 120, 130, 140]
        
        dd = self.calc.calculate_max_drawdown(equity)
        
        self.assertEqual(dd, 0.0)
    
    def test_calmar_ratio(self):
        returns = [0.001] * 52  # ~5% annual
        equity = [10000 + i*10 for i in range(53)]
        
        calmar = self.calc.calculate_calmar_ratio(returns, equity)
        
        self.assertGreaterEqual(calmar, 0)

if __name__ == "__main__":
    unittest.main()
