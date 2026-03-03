"""
Utility Functions
Helper functions for logging, formatting, and calculations
"""

import logging
from datetime import datetime
from typing import Optional

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Configure logger with consistent formatting"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

def format_currency(amount: float, precision: int = 2) -> str:
    """Format number as currency"""
    return f"${amount:,.{precision}f}"

def format_percent(value: float, precision: int = 2) -> str:
    """Format decimal as percentage"""
    return f"{value * 100:.{precision}f}%"

def calculate_dte(expiration_date: str) -> int:
    """Calculate days to expiration"""
    exp = datetime.strptime(expiration_date, "%Y-%m-%d")
    today = datetime.now()
    return max(0, (exp - today).days)

def annualized_return(weekly_yield: float) -> float:
    """Convert weekly yield to annualized"""
    return (1 + weekly_yield) ** 52 - 1

def is_market_hours() -> bool:
    """Check if current time is during market hours (9:30 AM - 4:00 PM EST)"""
    now = datetime.now()
    
    # Check if weekday (Monday = 0, Friday = 4)
    if now.weekday() > 4:
        return False
    
    # Simple check - doesn't account for timezone
    # In production, use proper timezone handling
    hour = now.hour
    return 9 <= hour < 16

class Colors:
    """Terminal colors for output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    
    @classmethod
    def colorize(cls, text: str, color: str) -> str:
        return f"{color}{text}{cls.END}"

if __name__ == "__main__":
    # Demo
    logger = setup_logger("kelvin")
    logger.info("Logger initialized")
    
    print(f"Currency: {format_currency(12345.67)}")
    print(f"Percent: {format_percent(0.0725)}")
    print(f"DTE for 2026-03-15: {calculate_dte('2026-03-15')} days")
    print(f"Annualized: {format_percent(annualized_return(0.01))}")
    print(f"Market hours: {is_market_hours()}")
    
    print(Colors.colorize("Success!", Colors.GREEN))
    print(Colors.colorize("Warning!", Colors.YELLOW))
    print(Colors.colorize("Error!", Colors.RED))
