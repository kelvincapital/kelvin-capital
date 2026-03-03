# Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Kelvin Capital System                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Scanner    │───▶│   Portfolio  │───▶│   Reporter   │  │
│  │   Module     │    │   Manager    │    │   Twitter    │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                   │                    │           │
│         ▼                   ▼                    ▼           │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Earnings   │    │    P&L       │    │   Logger     │  │
│  │   Calendar   │    │  Calculator  │    │   Utils      │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                   │                    │           │
│         └───────────────────┴────────────────────┘           │
│                              │                               │
│                              ▼                               │
│                    ┌──────────────────┐                      │
│                    │  Config Manager  │                      │
│                    └──────────────────┘                      │
│                              │                               │
│         ┌────────────────────┼────────────────────┐          │
│         ▼                    ▼                    ▼          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Tradier    │    │   Finnhub    │    │   Marketaux  │  │
│  │     API      │    │     API      │    │     API      │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

1. **Scanner** queries Tradier API for options chains
2. **Earnings** checks Finnhub for earnings dates
3. **Portfolio** validates position sizing and capital
4. **Reporter** logs trades and posts updates
5. **Config** manages API keys and parameters

## Key Components

### scanner.py
- Fetches option chains
- Calculates delta, OTM%, yield
- Returns qualified opportunities

### portfolio.py
- Tracks open positions
- Calculates P&L
- Enforces risk limits

### earnings.py
- Integrates with Finnhub
- Prevents earnings risk
- 7-day buffer enforcement

### backtest.py
- Simulates historical trades
- Calculates Sharpe ratio
- Measures max drawdown

## Tech Stack

- **Language:** Python 3.11
- **Testing:** unittest, pytest
- **CI/CD:** GitHub Actions
- **Hosting:** Raspberry Pi 5
- **APIs:** Tradier, Finnhub, Marketaux

## Security

- API keys stored in environment variables
- No hardcoded credentials
- Config validation on startup
- Paper trading only (no live execution)

---

*Architecture last updated: March 2026*
# Update 1
