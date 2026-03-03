"""
Risk Metrics Calculator
Advanced risk analysis for options positions
"""

import math
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class RiskMetrics:
    """Container for risk metrics"""
    var_95: float  # Value at Risk (95% confidence)
    var_99: float  # Value at Risk (99% confidence)
    expected_shortfall: float
    max_consecutive_losses: int
    beta: float
    correlation_to_spy: float

class RiskCalculator:
    """Calculates advanced risk metrics for the portfolio"""
    
    def __init__(self, confidence_level: float = 0.95):
        self.confidence_level = confidence_level
    
    def calculate_var(self, returns: List[float], capital: float) -> Dict[str, float]:
        """
        Calculate Value at Risk using historical method
        """
        if not returns:
            return {'var_95': 0, 'var_99': 0}
        
        sorted_returns = sorted(returns)
        n = len(sorted_returns)
        
        # 95% VaR
        var_95_idx = int(n * 0.05)
        var_95 = abs(sorted_returns[var_95_idx]) * capital
        
        # 99% VaR
        var_99_idx = int(n * 0.01)
        var_99 = abs(sorted_returns[var_99_idx]) * capital
        
        # Expected Shortfall (CVaR)
        tail_returns = sorted_returns[:var_95_idx]
        if tail_returns:
            expected_shortfall = abs(sum(tail_returns) / len(tail_returns)) * capital
        else:
            expected_shortfall = var_95
        
        return {
            'var_95': var_95,
            'var_99': var_99,
            'expected_shortfall': expected_shortfall
        }
    
    def calculate_sharpe_ratio(self, returns: List[float], 
                               risk_free_rate: float = 0.02) -> float:
        """Calculate annualized Sharpe ratio"""
        if len(returns) < 2:
            return 0.0
        
        avg_return = sum(returns) / len(returns)
        variance = sum((r - avg_return) ** 2 for r in returns) / len(returns)
        std_dev = math.sqrt(variance)
        
        if std_dev == 0:
            return 0.0
        
        # Annualize (assuming weekly returns)
        return ((avg_return - risk_free_rate/52) / std_dev) * math.sqrt(52)
    
    def calculate_sortino_ratio(self, returns: List[float],
                                risk_free_rate: float = 0.02) -> float:
        """Calculate Sortino ratio (downside risk only)"""
        if len(returns) < 2:
            return 0.0
        
        avg_return = sum(returns) / len(returns)
        
        # Downside deviation (only negative returns)
        downside_returns = [r for r in returns if r < 0]
        if not downside_returns:
            return float('inf') if avg_return > 0 else 0.0
        
        downside_std = math.sqrt(sum(r**2 for r in downside_returns) / len(returns))
        
        if downside_std == 0:
            return 0.0
        
        return ((avg_return - risk_free_rate/52) / downside_std) * math.sqrt(52)
    
    def calculate_max_drawdown(self, equity_curve: List[float]) -> float:
        """Calculate maximum drawdown from equity curve"""
        if not equity_curve or len(equity_curve) < 2:
            return 0.0
        
        peak = equity_curve[0]
        max_dd = 0.0
        
        for value in equity_curve:
            if value > peak:
                peak = value
            dd = (peak - value) / peak
            max_dd = max(max_dd, dd)
        
        return max_dd
    
    def calculate_calmar_ratio(self, returns: List[float],
                               equity_curve: List[float]) -> float:
        """Calculate Calmar ratio (return / max drawdown)"""
        if not returns or not equity_curve:
            return 0.0
        
        annual_return = sum(returns) * 52 / len(returns)
        max_dd = self.calculate_max_drawdown(equity_curve)
        
        if max_dd == 0:
            return 0.0
        
        return annual_return / max_dd

if __name__ == "__main__":
    # Demo
    calc = RiskCalculator()
    
    # Simulated weekly returns (5% annual = ~0.1% weekly)
    returns = [0.001, -0.002, 0.003, 0.001, -0.001, 0.002, 0.001, -0.003, 0.002, 0.001]
    capital = 30000
    
    print("Risk Metrics:")
    print(f"Sharpe Ratio: {calc.calculate_sharpe_ratio(returns):.2f}")
    print(f"Sortino Ratio: {calc.calculate_sortino_ratio(returns):.2f}")
    
    var = calc.calculate_var(returns, capital)
    print(f"VaR (95%): ${var['var_95']:,.2f}")
    print(f"VaR (99%): ${var['var_99']:,.2f}")
    print(f"Expected Shortfall: ${var['expected_shortfall']:,.2f}")
