"""
Earnings Calendar Integration
Prevents trading during earnings periods
"""

import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class EarningsCalendar:
    """Checks for upcoming earnings dates"""
    
    def __init__(self, finnhub_token: str):
        self.token = finnhub_token
        self.base_url = "https://finnhub.io/api/v1"
    
    def get_earnings_date(self, ticker: str) -> Optional[str]:
        """Get next earnings date for a ticker"""
        url = f"{self.base_url}/stock/earnings"
        params = {
            "symbol": ticker,
            "token": self.token
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if 'earningsCalendar' in data and len(data['earningsCalendar']) > 0:
                # Get most recent/future earnings
                earnings = data['earningsCalendar'][0]
                return earnings.get('date')
            
            return None
        except Exception as e:
            print(f"Error fetching earnings for {ticker}: {e}")
            return None
    
    def is_safe_to_trade(self, ticker: str, days_buffer: int = 7) -> bool:
        """
        Check if it's safe to trade (no earnings within buffer days)
        Returns True if safe, False if earnings is too close
        """
        earnings_date = self.get_earnings_date(ticker)
        
        if earnings_date is None:
            return True  # No earnings data, assume safe
        
        try:
            earnings = datetime.strptime(earnings_date, "%Y-%m-%d")
            today = datetime.now()
            days_until = (earnings - today).days
            
            # Safe if earnings is more than buffer days away
            return days_until > days_buffer or days_until < -1  # Already passed
        except:
            return True
    
    def get_upcoming_earnings(self, tickers: List[str], days_ahead: int = 30) -> Dict[str, str]:
        """Get earnings dates for multiple tickers"""
        upcoming = {}
        
        for ticker in tickers:
            date = self.get_earnings_date(ticker)
            if date:
                try:
                    earnings = datetime.strptime(date, "%Y-%m-%d")
                    today = datetime.now()
                    days_until = (earnings - today).days
                    
                    if 0 <= days_until <= days_ahead:
                        upcoming[ticker] = date
                except:
                    continue
        
        return upcoming

if __name__ == "__main__":
    # Demo
    calendar = EarningsCalendar("your_token_here")
    
    # Check single ticker
    safe = calendar.is_safe_to_trade("AAPL", days_buffer=7)
    print(f"Safe to trade AAPL: {safe}")
    
    # Check earnings date
    date = calendar.get_earnings_date("AAPL")
    print(f"AAPL earnings: {date}")
