# Kelvin Capital — CSP Rules & Criteria

## Underlying Requirements

✅ **Must be S&P 500 constituent**
- 500 eligible tickers
- ETFs allowed: SPY, QQQ, IWM, DIA

✅ **Liquidity Requirements**
- Tight bid/ask spreads (< 10% of option price)
- Minimum daily volume: 1M+ shares
- Active options chain (open interest > 100)

❌ **Avoid These**
- Binary/event-driven risk (biotech FDA decisions, mergers)
- Low liquidity (< 500K daily volume)
- Wide bid/ask spreads (> 15% of option price)

## Contract Requirements

### Strike Selection
- **Minimum:** 10% OTM from current price
- **Preferred:** 15-20% OTM (safer buffer)
- **Example:** Stock at $100 → Strike ≤ $90

### Yield Targets
- **Minimum:** 0.7% return per week
- **Target:** 1.0%+ return per week
- **Exceptional:** 1.5%+ (rare, high IV environment)

### Delta Range
- **Target:** 0.20 – 0.35
- **Conservative:** 0.15 – 0.25
- **Aggressive:** 0.30 – 0.40 (only in bull markets)

### Expiration
- **Sweet Spot:** 7-14 days to expiration (DTE)
- **Minimum:** 5 DTE (too much gamma risk)
- **Maximum:** 21 DTE (ties up capital too long)

### Premium
- **Minimum:** $0.50 per contract (commissions eat small premiums)
- **Preferred:** $1.00+ per contract

## Earnings Calendar Check

❌ **NO TRADES within 3 days of earnings**
- High volatility crush risk
- Binary outcome (big move either direction)
- Check earnings calendar before entering any position

✅ **Safe Windows**
- 4+ days after earnings
- 7+ days before next earnings

## Risk Management

### Position Sizing
- **Max per underlying:** 5% of account
- **Max per sector:** 20% of account
- **Max total:** 50% of account (keep 50% cash)

### Assignment Plan
If assigned:
1. Evaluate if want to own stock at strike price
2. If yes: Keep shares, sell covered calls (wheel strategy)
3. If no: Sell shares immediately, take loss, redeploy capital

### Mental Stops
- **Close early if:** Stock drops > 20% from entry
- **Roll if:** 3-5 DTE and ITM, but still believe in thesis
- **Take profit early:** If 50%+ of premium captured with > 50% time remaining

## Quick Screening Checklist

Before entering any CSP:

- [ ] S&P 500 constituent?
- [ ] Earnings > 7 days away?
- [ ] Strike 10%+ OTM?
- [ ] Delta 0.20-0.35?
- [ ] 7-14 DTE?
- [ ] Premium yield ≥ 0.7%/week?
- [ ] Tight bid/ask spread?
- [ ] No binary event risk?

**All checked = Valid candidate**

## Calculation Formula

**Weekly Return % = (Premium / Capital Required) × (7 / DTE)**

Where:
- Premium = Credit received
- Capital Required = Strike Price × 100 (per contract)
- DTE = Days to expiration

### Example:
Stock: $120
Strike: $108 (10% OTM)
Premium: $1.20
DTE: 14

Capital Required: $10,800
Return: $120 / $10,800 = 1.11%
Weekly Return: 1.11% × (7/14) = **0.56% per week** ❌ (below 0.7% minimum)

