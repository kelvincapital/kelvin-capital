"""
Portfolio Manager
Tracks positions, P&L, and risk metrics
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum
import json

class PositionStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"
    EXPIRED = "expired"
    ASSIGNED = "assigned"

@dataclass
class Position:
    """Single trade position"""
    id: str
    ticker: str
    position_type: str  # 'CSP' or 'CC'
    strike: float
    expiration: str
    entry_date: datetime
    contracts: int
    premium_received: float
    status: PositionStatus = PositionStatus.OPEN
    exit_date: Optional[datetime] = None
    exit_price: Optional[float] = None
    pnl: Optional[float] = None
    notes: str = ""
    
    @property
    def days_held(self) -> int:
        if self.exit_date:
            return (self.exit_date - self.entry_date).days
        return (datetime.now() - self.entry_date).days
    
    @property
    def capital_at_risk(self) -> float:
        return self.strike * 100 * self.contracts
    
    @property
    def return_pct(self) -> Optional[float]:
        if self.pnl is None:
            return None
        return self.pnl / self.capital_at_risk

class Portfolio:
    """Manages all trading positions"""
    
    def __init__(self, initial_capital: float = 30000.0):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions: List[Position] = []
        self.trade_history: List[Position] = []
        self.position_counter = 0
    
    def add_position(self, ticker: str, position_type: str, strike: float,
                     expiration: str, contracts: int, premium: float) -> Position:
        """Add a new position"""
        self.position_counter += 1
        
        position = Position(
            id=f"TRADE_{self.position_counter:04d}",
            ticker=ticker,
            position_type=position_type,
            strike=strike,
            expiration=expiration,
            entry_date=datetime.now(),
            contracts=contracts,
            premium_received=premium
        )
        
        self.positions.append(position)
        self.cash += premium  # Premium received increases cash
        
        return position
    
    def close_position(self, position_id: str, exit_price: float, 
                       notes: str = "") -> Optional[Position]:
        """Close an open position"""
        for pos in self.positions:
            if pos.id == position_id:
                pos.exit_date = datetime.now()
                pos.exit_price = exit_price
                pos.status = PositionStatus.CLOSED
                pos.pnl = (pos.premium_received - exit_price) * pos.contracts * 100
                pos.notes = notes
                
                self.cash -= exit_price * pos.contracts * 100  # Buyback cost
                self.trade_history.append(pos)
                self.positions.remove(pos)
                
                return pos
        return None
    
    def get_open_positions(self) -> List[Position]:
        """Get all open positions"""
        return [p for p in self.positions if p.status == PositionStatus.OPEN]
    
    def get_metrics(self) -> Dict:
        """Calculate portfolio metrics"""
        open_positions = self.get_open_positions()
        closed_positions = self.trade_history
        
        total_pnl = sum(p.pnl for p in closed_positions if p.pnl)
        wins = sum(1 for p in closed_positions if p.pnl and p.pnl > 0)
        losses = sum(1 for p in closed_positions if p.pnl and p.pnl <= 0)
        total_trades = wins + losses
        
        return {
            'initial_capital': self.initial_capital,
            'current_cash': self.cash,
            'total_value': self.cash + sum(p.capital_at_risk for p in open_positions),
            'open_positions': len(open_positions),
            'total_trades': total_trades,
            'win_rate': wins / total_trades if total_trades > 0 else 0,
            'total_pnl': total_pnl,
            'return_pct': total_pnl / self.initial_capital if self.initial_capital else 0,
            'avg_trade_return': total_pnl / total_trades if total_trades > 0 else 0
        }
    
    def export_to_json(self, filepath: str):
        """Export portfolio to JSON"""
        data = {
            'initial_capital': self.initial_capital,
            'current_cash': self.cash,
            'positions': [
                {
                    'id': p.id,
                    'ticker': p.ticker,
                    'type': p.position_type,
                    'strike': p.strike,
                    'expiration': p.expiration,
                    'premium': p.premium_received,
                    'status': p.status.value,
                    'pnl': p.pnl
                } for p in self.positions + self.trade_history
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    # Demo
    portfolio = Portfolio(initial_capital=30000)
    
    # Add a position
    pos = portfolio.add_position(
        ticker="AAPL",
        position_type="CSP",
        strike=150.0,
        expiration="2026-03-21",
        contracts=1,
        premium=125.0
    )
    
    print(f"Added position: {pos.id}")
    print(f"Open positions: {len(portfolio.get_open_positions())}")
    print(f"Cash: ${portfolio.cash:.2f}")
    
    # Get metrics
    metrics = portfolio.get_metrics()
    print(f"\nPortfolio Metrics:")
    for key, val in metrics.items():
        if isinstance(val, float):
            print(f"  {key}: {val:.2%}" if 'pct' in key or 'rate' in key else f"  {key}: ${val:,.2f}")
        else:
            print(f"  {key}: {val}")
