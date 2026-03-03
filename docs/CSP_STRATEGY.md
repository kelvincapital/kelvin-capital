# Cash Secured Put (CSP) Strategy Guide

## What is a Cash Secured Put?

A Cash Secured Put is an options strategy where you:
1. **Sell** a put option on a stock you want to own
2. **Collect** the premium immediately
3. **Keep** cash available to buy shares if assigned

If the stock stays above the strike price: You keep the premium, no shares bought.  
If the stock drops below the strike: You buy shares at the strike price (minus premium received).

## Why CSPs?

**Advantages:**
- Generate income from premiums
- Get paid to wait for stocks you want to own
- Lower risk than buying stock outright
- Defined risk (you know max loss upfront)

**Ideal Market Conditions:**
- High implied volatility (IV) = higher premiums
- Bullish to neutral outlook
- Stocks you actually want to own long-term

## The Wheel Strategy

The Wheel combines CSPs with Covered Calls:

1. **Phase 1:** Sell CSPs until assigned (collecting premiums)
2. **Phase 2:** Once assigned, sell Covered Calls on those shares
3. **Repeat:** If called away, sell CSPs again

This generates income in both directions — whether you own the stock or not.

## Kelvin Capital's Approach

### Selection Criteria
- **Underlying:** S&P 500 stocks only (quality companies)
- **Strike:** 10%+ OTM (safety buffer)
- **Delta:** 0.20-0.35 (probability sweet spot)
- **DTE:** 7-14 days (time decay acceleration)
- **Yield:** Minimum 0.7% per week

### Risk Management
- No earnings within 7 days
- Check for upcoming events/news
- Position sizing: Max 5% per trade
- Mental stops: Close if down 20%

### Assignment Plan
If assigned shares:
1. Evaluate if still bullish on company
2. If yes: Keep shares, sell Covered Calls
3. If no: Sell immediately, take loss, move on

## Example Trade

**Setup:**
- Stock: XYZ at $100
- Sell: $90 put (10% OTM)
- Expiration: 14 days
- Premium: $0.70
- Delta: 0.25

**Outcomes:**
- **XYZ stays > $90:** Keep $0.70 premium (0.78% return in 2 weeks)
- **XYZ drops to $85:** Buy shares at $90, cost basis = $89.30 ($90 - $0.70 premium)

## Key Metrics

**Return on Capital (ROC):**
```
ROC = (Premium / Strike Price) × 100
```

**Weekly Yield:**
```
Weekly Yield = ROC ÷ (DTE / 7)
```

**Breakeven:**
```
Breakeven = Strike Price - Premium
```

## Common Mistakes to Avoid

1. **Selling CSPs on stocks you don't want to own**
2. **Ignoring earnings dates** (volatility crush risk)
3. **Chasing yield** (high premiums = high risk)
4. **Poor position sizing** (too much capital in one trade)
5. **Not having exit plan** before entering

## Resources

- [Options Basics - Investopedia](https://www.investopedia.com/options-basics-4689239)
- [CSP Strategy Guide - Option Alpha](https://optionalpha.com/)
- [Wheel Strategy Explained](https://www.youtube.com/watch?v=wheel-strategy)

---

*Remember: This is educational content. Not financial advice. Options trading involves substantial risk.*

## Resources

- [Options Industry Council](https://www.optionseducation.org/)
- [CBOE Education](https://www.cboe.com/education/)
