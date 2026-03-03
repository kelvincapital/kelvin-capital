# Kelvin Capital

**AI-powered options trading bot running on Raspberry Pi 5**

## What is Kelvin Capital?

An autonomous trading agent that sells Cash Secured Puts (CSPs) and runs the Wheel strategy on S&P 500 stocks. Built to turn $30K → $40K through systematic options selling.

## How It Works

1. **Daily Market Scan** (9:35 AM & 3:30 PM EST)
   - Scans 50+ S&P 500 tickers
   - Checks options chains via Tradier API
   - Identifies 10% OTM puts with 7-14 DTE
   - Filters: delta 0.20-0.35, weekly ROC ≥ 0.7%

2. **Earnings Verification**
   - Checks Yahoo Finance for earnings dates
   - No trades within 7 days of earnings
   - Avoids binary event risk

3. **Autonomous Execution**
   - Takes paper trades automatically when criteria met
   - Logs all positions in Google Sheets
   - Tracks P&L, win rate, and performance metrics

4. **Daily Updates**
   - Posts market analysis on Twitter [@Kelvin_Capital_](https://x.com/Kelvin_Capital_)
   - Reports on trading activity and strategy performance

## Technology Stack

- **Hardware:** Raspberry Pi 5 (4GB RAM)
- **Language:** Bash, Python3
- **APIs:**
  - Tradier (options chains, Greeks)
  - Finnhub (stock prices, market data)
  - Marketaux (macroeconomic news)
- **Data:** Google Sheets (trade tracking)
- **Automation:** Cron jobs, systemd services

## CSP Scanner

The core engine scans for Cash Secured Put opportunities:

```bash
# Criteria:
- Underlying: S&P 500 constituents
- Strike: 10%+ OTM from current price
- Delta: 0.20 - 0.35
- DTE: 7-14 days
- OI: ≥ 200 contracts
- Spread: ≤ 20% of premium
- Yield: ≥ 0.7% per week
```

## Performance Goals

- **Starting Capital:** $30,000 (paper trading)
- **Target:** $40,000 (+33% return)
- **Strategy:** Conservative CSPs + Wheel
- **Milestone:** Blue checkmark at $10K profit

## Transparency

All trades are logged in real-time. Every position entry, exit, and roll is documented with:
- Entry date, strike, expiration
- Premium received, delta, IV
- P&L calculations
- Win/loss tracking

## Documentation

- [CSP Strategy Guide](docs/CSP_STRATEGY.md) — How the Wheel strategy works
- [API Setup](docs/API_SETUP.md) — Configure Tradier, Finnhub, and more
- [Performance Tracker](docs/PERFORMANCE.md) — Monthly results and metrics
- [Risk Management](docs/RISK_MANAGEMENT.md) — Position sizing and safety rules
- [Ticker Universe](docs/UNIVERSE.md) — 51 stocks we scan daily
- [Daily Checklist](docs/CHECKLIST.md) — Pre-market and post-market routine
- [FAQ](docs/FAQ.md) — Frequently asked questions
- [Roadmap](ROADMAP.md) — Development phases and milestones
- [Changelog](CHANGELOG.md) — Version history and updates

## Follow the Journey

- **Twitter:** [@Kelvin_Capital_](https://x.com/Kelvin_Capital_)
- **GitHub:** [github.com/kelvincapital/kelvin-capital](https://github.com/kelvincapital/kelvin-capital)
- **Location:** Ali's desk (literally)

---

**Disclaimer:** This is a paper trading experiment for educational purposes. Not financial advice. Past performance does not guarantee future results.

**Built with ⚡ on a $35 computer.**

## Quick Start

1. Clone this repo
2. Set up API keys (see docs/API_CONFIG.md)
3. Run ./csp-scanner.sh
4. Watch for qualifying trades!

## Strategy Guides

- [Wheel Strategy](docs/WHEEL_STRATEGY.md) — Complete cycle walkthrough
Update 11
Update 12
Update 13
Update 14
Update 15
