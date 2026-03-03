"""
CSP Scanner Core Algorithm
Kelvin Capital - AI-Powered Options Trading

This module implements the Cash Secured Put scanning algorithm
with delta targeting, risk management, and position sizing.
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class TradeStatus(Enum):
    QUALIFIED = "qualified"
    REJECTED = "rejected"
    PENDING = "pending"

@dataclass
class CSPParameters:
    """Parameters for CSP trade evaluation"""
    min_otm_percent: float = 10.0
    max_otm_percent: float = 15.0
    min_delta: float = 0.20
    max_delta: float = 0.35
    min_dte: int = 7
    max_dte: int = 14
    min_weekly_yield: float = 0.007  # 0.7%
    min_open_interest: int = 200

@dataclass
class OptionContract:
    """Represents an option contract"""
    symbol: str
    strike: float
    expiration: str
    bid: float
    ask: float
    delta: float
    gamma: float
    theta: float
    vega: float
    iv: float
    open_interest: int
    volume: int
    
    @property
    def mid_price(self) -> float:
        return (self.bid + self.ask) / 2
    
    @property
    def spread_percent(self) -> float:
        if self.mid_price == 0:
            return float('inf')
        return (self.ask - self.bid) / self.mid_price

@dataclass  
class TradeOpportunity:
    """Evaluated trade opportunity"""
    ticker: str
    current_price: float
    contract: OptionContract
    otm_percent: float
    weekly_yield: float
    annualized_yield: float
    status: TradeStatus
    rejection_reason: Optional[str] = None

class CSPScanner:
    """
    Core scanner for Cash Secured Put opportunities.
    
    Implements the Kelvin Capital trading strategy:
    - Sells puts 10-15% OTM
    - Delta range: 0.20-0.35
    - DTE: 7-14 days
    - Minimum 0.7% weekly yield
    """
    
    def __init__(self, tradier_token: str, finnhub_token: str):
        self.tradier_token = tradier_token
        self.finnhub_token = finnhub_token
        self.tradier_base = "https://sandbox.tradier.com/v1"
        self.finnhub_base = "https://finnhub.io/api/v1"
        self.params = CSPParameters()
        
    def get_stock_price(self, ticker: str) -> Optional[float]:
        """Fetch current stock price from Finnhub"""
        url = f"{self.finnhub_base}/quote"
        params = {"symbol": ticker, "token": self.finnhub_token}
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            return data.get('c')
        except Exception as e:
            print(f"Error fetching price for {ticker}: {e}")
            return None
    
    def get_option_expirations(self, ticker: str) -> List[str]:
        """Get available option expiration dates"""
        url = f"{self.tradier_base}/markets/options/expirations"
        headers = {"Authorization": f"Bearer {self.tradier_token}"}
        params = {"symbol": ticker}
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            data = response.json()
            
            if 'expirations' not in data or 'date' not in data['expirations']:
                return []
            
            dates = data['expirations']['date']
            if isinstance(dates, str):
                dates = [dates]
            
            # Filter for 7-14 DTE
            valid_dates = []
            today = datetime.now()
            
            for date_str in dates:
                exp_date = datetime.strptime(date_str, "%Y-%m-%d")
                dte = (exp_date - today).days
                if self.params.min_dte <= dte <= self.params.max_dte:
                    valid_dates.append(date_str)
            
            return valid_dates[:3]  # Top 3 valid expirations
            
        except Exception as e:
            print(f"Error fetching expirations for {ticker}: {e}")
            return []
    
    def get_option_chain(self, ticker: str, expiration: str) -> List[OptionContract]:
        """Fetch option chain for a specific expiration"""
        url = f"{self.tradier_base}/markets/options/chains"
        headers = {"Authorization": f"Bearer {self.tradier_token}"}
        params = {
            "symbol": ticker,
            "expiration": expiration,
            "greeks": "true"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
            data = response.json()
            
            contracts = []
            if 'options' in data and 'option' in data['options']:
                for opt in data['options']['option']:
                    if opt.get('option_type') != 'put':
                        continue
                    
                    greeks = opt.get('greeks', {})
                    contract = OptionContract(
                        symbol=opt.get('symbol', ''),
                        strike=float(opt.get('strike', 0)),
                        expiration=expiration,
                        bid=float(opt.get('bid', 0)),
                        ask=float(opt.get('ask', 0)),
                        delta=float(greeks.get('delta', 0)),
                        gamma=float(greeks.get('gamma', 0)),
                        theta=float(greeks.get('theta', 0)),
                        vega=float(greeks.get('vega', 0)),
                        iv=float(greeks.get('mid_iv', 0)),
                        open_interest=int(opt.get('open_interest', 0)),
                        volume=int(opt.get('volume', 0))
                    )
                    contracts.append(contract)
            
            return contracts
            
        except Exception as e:
            print(f"Error fetching chain for {ticker}: {e}")
            return []
    
    def evaluate_contract(self, ticker: str, current_price: float, 
                         contract: OptionContract) -> TradeOpportunity:
        """Evaluate if a contract meets CSP criteria"""
        
        # Calculate metrics
        otm_percent = ((current_price - contract.strike) / current_price) * 100
        dte = 10  # Approximate, would calculate from actual dates
        
        # Calculate weekly yield
        capital_required = contract.strike * 100  # 100 shares per contract
        weekly_yield = (contract.mid_price * 100) / capital_required
        if dte > 0:
            weekly_yield = weekly_yield / (dte / 7)
        
        annualized_yield = weekly_yield * 52
        
        # Evaluate criteria
        rejection_reasons = []
        
        if otm_percent < self.params.min_otm_percent:
            rejection_reasons.append(f"OTM {otm_percent:.1f}% < {self.params.min_otm_percent}%")
        elif otm_percent > self.params.max_otm_percent:
            rejection_reasons.append(f"OTM {otm_percent:.1f}% > {self.params.max_otm_percent}%")
        
        if abs(contract.delta) < self.params.min_delta:
            rejection_reasons.append(f"Delta {abs(contract.delta):.2f} < {self.params.min_delta}")
        elif abs(contract.delta) > self.params.max_delta:
            rejection_reasons.append(f"Delta {abs(contract.delta):.2f} > {self.params.max_delta}")
        
        if contract.open_interest < self.params.min_open_interest:
            rejection_reasons.append(f"OI {contract.open_interest} < {self.params.min_open_interest}")
        
        if weekly_yield < self.params.min_weekly_yield:
            rejection_reasons.append(f"Yield {weekly_yield:.2%} < {self.params.min_weekly_yield:.2%}")
        
        if contract.spread_percent > 0.20:
            rejection_reasons.append(f"Spread {contract.spread_percent:.1%} > 20%")
        
        status = TradeStatus.REJECTED if rejection_reasons else TradeStatus.QUALIFIED
        
        return TradeOpportunity(
            ticker=ticker,
            current_price=current_price,
            contract=contract,
            otm_percent=otm_percent,
            weekly_yield=weekly_yield,
            annualized_yield=annualized_yield,
            status=status,
            rejection_reason="; ".join(rejection_reasons) if rejection_reasons else None
        )
    
    def scan_ticker(self, ticker: str) -> List[TradeOpportunity]:
        """Scan a single ticker for CSP opportunities"""
        opportunities = []
        
        # Get current price
        current_price = self.get_stock_price(ticker)
        if current_price is None:
            return []
        
        print(f"\nScanning {ticker} @ ${current_price:.2f}")
        
        # Get valid expirations
        expirations = self.get_option_expirations(ticker)
        if not expirations:
            print(f"  No valid expirations found")
            return []
        
        # Scan each expiration
        for exp in expirations:
            contracts = self.get_option_chain(ticker, exp)
            print(f"  Exp {exp}: {len(contracts)} puts")
            
            for contract in contracts:
                opp = self.evaluate_contract(ticker, current_price, contract)
                opportunities.append(opp)
        
        return opportunities
    
    def scan_universe(self, tickers: List[str]) -> List[TradeOpportunity]:
        """Scan entire universe and return qualified opportunities"""
        all_opportunities = []
        
        print(f"\n{'='*60}")
        print("KELVIN CAPITAL CSP SCANNER")
        print(f"Scanning {len(tickers)} tickers...")
        print(f"{'='*60}")
        
        for ticker in tickers:
            opps = self.scan_ticker(ticker)
            all_opportunities.extend(opps)
        
        # Filter to only qualified
        qualified = [o for o in all_opportunities if o.status == TradeStatus.QUALIFIED]
        
        # Sort by weekly yield (highest first)
        qualified.sort(key=lambda x: x.weekly_yield, reverse=True)
        
        print(f"\n{'='*60}")
        print(f"SCAN COMPLETE")
        print(f"Total evaluated: {len(all_opportunities)}")
        print(f"Qualified trades: {len(qualified)}")
        print(f"{'='*60}")
        
        return qualified


if __name__ == "__main__":
    # Example usage
    scanner = CSPScanner(
        tradier_token="your_token_here",
        finnhub_token="your_token_here"
    )
    
    # Small test universe
    test_tickers = ["AAPL", "TSLA", "AMD"]
    
    results = scanner.scan_universe(test_tickers)
    
    print("\nTOP OPPORTUNITIES:")
    for opp in results[:5]:
        print(f"\n{opp.ticker} ${opp.contract.strike} Put")
        print(f"  Exp: {opp.contract.expiration}")
        print(f"  Premium: ${opp.contract.mid_price:.2f}")
        print(f"  Delta: {abs(opp.contract.delta):.2f}")
        print(f"  OTM: {opp.otm_percent:.1f}%")
        print(f"  Weekly Yield: {opp.weekly_yield:.2%}")
        print(f"  Annualized: {opp.annualized_yield:.0%}")
