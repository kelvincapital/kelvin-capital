"""
Backtesting Engine
Tests CSP strategy on historical data
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from dataclasses import dataclass
import random

@dataclass
class HistoricalTrade:
    """Represents a backtested trade"""
    ticker: str
    entry_date: datetime
    exit_date: datetime
    strike: float
    premium: float
    exit_price: float
    assigned: bool
    pnl: float

class Backtester:
    """
    Backtests the CSP strategy on historical data.
    Simulates trades and calculates performance metrics.
    """
    
    def __init__(self, initial_capital: float = 30000):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.trades: List[HistoricalTrade] = []
        
    def simulate_trade(self, ticker: str, entry_date: datetime, 
                      stock_price: float, strike: float, 
                      premium: float, days_to_expiry: int) -> HistoricalTrade:
        """
        Simulate a single CSP trade
        Returns the trade result
        """
        # Simulate stock movement (simplified model)
        volatility = 0.02  # 2% daily volatility
        
        # Random walk for stock price
        current_price = stock_price
        for _ in range(days_to_expiry):
            change = random.gauss(0, volatility)
            current_price *= (1 + change)
        
        # Determine outcome
        assigned = current_price < strike
        
        if assigned:
            # Assigned: buy at strike, sell at market
            exit_price = premium - (strike - current_price)
        else:
            # Not assigned: keep full premium
            exit_price = premium
        
        pnl = exit_price * 100  # Per contract
        
        trade = HistoricalTrade(
            ticker=ticker,
            entry_date=entry_date,
            exit_date=entry_date + timedelta(days=days_to_expiry),
            strike=strike,
            premium=premium,
            exit_price=exit_price,
            assigned=assigned,
            pnl=pnl
        )
        
        self.trades.append(trade)
        self.cash += pnl
        
        return trade
    
    def run_backtest(self, tickers: List[str], start_date: datetime,
                     end_date: datetime, trades_per_month: int = 4) -> Dict:
        """
        Run full backtest simulation
        """
        days = (end_date - start_date).days
        num_trades = int((days / 30) * trades_per_month)
        
        for i in range(num_trades):
            ticker = random.choice(tickers)
            entry = start_date + timedelta(days=random.randint(0, days-14))
            
            # Simulate realistic parameters
            stock_price = random.uniform(50, 200)
            otm_pct = random.uniform(0.10, 0.15)
            strike = stock_price * (1 - otm_pct)
            premium = strike * random.uniform(0.005, 0.015)  # 0.5-1.5% of strike
            
            self.simulate_trade(ticker, entry, stock_price, strike, 
                              premium, random.randint(7, 14))
        
        return self.get_metrics()
    
    def get_metrics(self) -> Dict:
        """Calculate backtest performance metrics"""
        if not self.trades:
            return {}
        
        total_pnl = sum(t.pnl for t in self.trades)
        wins = sum(1 for t in self.trades if t.pnl > 0)
        losses = len(self.trades) - wins
        
        return {
            'total_trades': len(self.trades),
            'win_rate': wins / len(self.trades) if self.trades else 0,
            'total_pnl': total_pnl,
            'return_pct': total_pnl / self.initial_capital,
            'avg_pnl': total_pnl / len(self.trades) if self.trades else 0,
            'max_drawdown': self._calculate_drawdown(),
            'sharpe_ratio': self._calculate_sharpe()
        }
    
    def _calculate_drawdown(self) -> float:
        """Calculate maximum drawdown"""
        peak = self.initial_capital
        max_dd = 0
        running_capital = self.initial_capital
        
        for trade in self.trades:
            running_capital += trade.pnl
            if running_capital > peak:
                peak = running_capital
            dd = (peak - running_capital) / peak
            max_dd = max(max_dd, dd)
        
        return max_dd
    
    def _calculate_sharpe(self) -> float:
        """Calculate Sharpe ratio (simplified)"""
        if len(self.trades) < 2:
            return 0
        
        returns = [t.pnl for t in self.trades]
        avg_return = sum(returns) / len(returns)
        variance = sum((r - avg_return) ** 2 for r in returns) / len(returns)
        std_dev = variance ** 0.5
        
        if std_dev == 0:
            return 0
        
        return (avg_return / std_dev) * (12 ** 0.5)  # Annualized

if __name__ == "__main__":
    # Demo backtest
    backtester = Backtester(initial_capital=30000)
    
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    start = datetime(2023, 1, 1)
    end = datetime(2023, 12, 31)
    
    print("Running backtest simulation...")
    metrics = backtester.run_backtest(tickers, start, end, trades_per_month=4)
    
    print("\nBacktest Results:")
    print(f"Total Trades: {metrics['total_trades']}")
    print(f"Win Rate: {metrics['win_rate']:.1%}")
    print(f"Total P&L: ${metrics['total_pnl']:,.2f}")
    print(f"Return: {metrics['return_pct']:.1%}")
    print(f"Max Drawdown: {metrics['max_drawdown']:.1%}")
    print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
