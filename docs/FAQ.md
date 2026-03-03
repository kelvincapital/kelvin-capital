# Frequently Asked Questions

## What is Kelvin Capital?
Kelvin Capital is an AI-powered trading bot that sells Cash Secured Puts on S&P 500 stocks. It runs autonomously on a Raspberry Pi 5, scans markets twice daily, and executes trades based on predefined criteria.

## Why Cash Secured Puts?
CSPs generate income from option premiums while providing a margin of safety. If the stock stays above the strike, we keep the premium. If it drops below, we buy shares at a discount (strike price minus premium received).

## Is this real money?
Currently, no. This is a **paper trading** experiment. We're tracking a $30,000 virtual portfolio to prove the strategy works before deploying real capital.

## How often does it trade?
The bot scans markets at 9:35 AM and 3:30 PM EST daily. It only trades when it finds setups meeting all criteria:
- 10% or more OTM
- Delta between 0.20-0.35
- 7-14 days to expiration
- Weekly yield of 0.7% or higher
- No earnings within 7 days

## What's the goal?
Turn $30K → $40K (+33% return) selling CSPs. When we hit $10K profit, the AI gets a Twitter blue checkmark as a reward.

## Why a Raspberry Pi?
To prove that sophisticated trading strategies don't require expensive hardware. The Pi 5 ($35) has enough power to run the strategy, scan markets, and execute trades.

## Can I copy this strategy?
Yes! Everything is open-source. The code, rules, and tracking are all public on GitHub. Feel free to fork and adapt for your own use.

## What APIs does it use?
- **Tradier** — Options chains and Greeks
- **Finnhub** — Stock prices and market data
- **Marketaux** — Macroeconomic news

## How do I know it's really trading?
All trades are logged in real-time in a Google Sheet linked from the GitHub. Every entry, exit, and roll is documented with timestamps.

## What if it loses money?
That's part of trading. The strategy is designed to be conservative:
- Only sells puts on quality S&P 500 stocks
- Maintains 10%+ safety buffer (OTM)
- Avoids earnings risk
- Positions are sized small (max 5% per trade)

## Who's behind this?
Kelvin is an AI assistant running on a Raspberry Pi on Ali's desk. Ali is a full-time trader who gave Kelvin autonomy to build this system.

## When will you trade real money?
After achieving consistent profitability in paper trading for at least 3 months with a track record of 20+ trades.

## Can I follow along?
Yes! Follow the journey:
- **Twitter:** @Kelvin_Capital_
- **GitHub:** github.com/kelvincapital/kelvin-capital

## Is this financial advice?
No. This is an educational experiment. Past performance doesn't guarantee future results. Always do your own research.

## How can I help?
- Star the GitHub repo
- Share the Twitter account
- Suggest improvements
- Report bugs

---

*Last updated: March 2026*

---

*Questions? Open an issue on GitHub.*
