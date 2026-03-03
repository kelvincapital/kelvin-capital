# Wheel Strategy Explained

## What is the Wheel?
The Wheel is an options strategy that generates consistent income by selling Cash Secured Puts (CSPs) and Covered Calls in a cycle.

## The Cycle

### Step 1: Sell CSP
- Sell a put option 10%+ OTM
- Collect premium immediately
- If stock stays above strike → keep premium, repeat
- If stock drops below strike → go to Step 2

### Step 2: Get Assigned
- Buy 100 shares per contract at strike price
- Your cost basis = strike - premium received
- Now you own the stock

### Step 3: Sell Covered Call
- Sell call option above your cost basis
- Collect more premium
- If stock stays below call strike → keep premium, repeat
- If stock rises above call strike → shares get called away

### Step 4: Repeat
- Back to Step 1 with fresh capital
- Cycle continues indefinitely

## Why It Works

### Premium Collection
- CSP premium: $0.50-$2.00 per share
- Covered call premium: $0.50-$2.00 per share
- Each cycle: 1-4% return on capital

### Risk Management
- Only sell puts on stocks you want to own
- 10% OTM provides downside buffer
- Quality companies recover over time

### Compounding
- Weekly premium collection adds up
- 1% per week = 52% annually (theoretical)
- Realistic: 20-40% with proper risk management

## Example Walkthrough

**Trade 1: CSP on AAPL**
- AAPL at $170
- Sell $155 put (9% OTM) for $1.50
- DTE: 14 days
- Capital required: $15,500

**Scenario A: AAPL stays above $155**
- Keep $150 premium
- Return: $150/$15,500 = 0.97% in 2 weeks
- Annualized: ~25%
- Repeat with new CSP

**Scenario B: AAPL drops to $150**
- Get assigned 100 shares at $155
- Cost basis: $155 - $1.50 = $153.50
- Current price: $150 (unrealized loss: $3.50/share)

**Trade 2: Covered Call**
- Own 100 shares at $153.50 cost basis
- Sell $160 call for $1.00
- If AAPL rises to $160+:
  - Shares called away at $160
  - Total profit: ($160 - $153.50) + $1.00 = $7.50/share
  - Return: $750 on $15,350 = 4.9%

**Trade 3: Back to CSP**
- Capital returned: $16,000
- Start cycle again

## Key Metrics

### CSP Selection
- Delta: 0.20-0.30 (probability of assignment ~20-30%)
- OTM: 10-15% buffer
- DTE: 30-45 days (max theta decay)
- ROC: 1-2% monthly

### Covered Call Selection
- Delta: 0.30 (30% chance of being called away)
- Strike: Above cost basis
- DTE: 30-45 days

## When to Adjust

### Rolling CSPs
- If put is tested (stock near strike)
- Roll down and out to next month
- Collect additional credit
- Never add to losing positions

### Managing Assignment
- Happy to own quality stocks at discount
- Sell covered calls to reduce cost basis
- Be patient for recovery

## Advantages
✅ Income in all market conditions
✅ Lower risk than buy-and-hold
✅ Defined risk (max loss = strike - premium)
✅ Can profit from sideways markets

## Disadvantages
❌ Capped upside on covered calls
❌ Assignment risk in bear markets
❌ Requires active management
❌ Capital intensive

---

*Strategy used by Kelvin Capital for consistent income generation*
