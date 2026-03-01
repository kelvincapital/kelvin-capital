# API Configuration Guide

This document explains how to set up the APIs used by Kelvin Capital.

## Required APIs

### 1. Tradier API (Options Data)
**Purpose:** Options chains, Greeks, expirations
**Signup:** https://developer.tradier.com/
**Tier:** Sandbox (free) or Live (paid)
**Rate Limits:** 
- Sandbox: 60 calls/minute
- Live: 1,000+ calls/minute

**Setup:**
1. Create account at Tradier Developer
2. Generate API token
3. Replace `TRADIER_TOKEN` in `csp-scanner.sh`

**Endpoints Used:**
- `/v1/markets/quotes` - Stock prices
- `/v1/markets/options/expirations` - Available expirations
- `/v1/markets/options/chains` - Full options chain with Greeks

### 2. Finnhub API (Market Data)
**Purpose:** Stock prices, indices, basic fundamentals
**Signup:** https://finnhub.io/
**Tier:** Free tier (60 calls/minute)

**Setup:**
1. Sign up for free account
2. Get API key from dashboard
3. Replace `FINNHUB_TOKEN` in scripts

**Endpoints Used:**
- `/api/v1/quote` - Real-time quotes
- `/api/v1/stock/earnings` - Historical earnings

### 3. Marketaux API (News)
**Purpose:** Macroeconomic news and sentiment
**Signup:** https://www.marketaux.com/
**Tier:** Free tier available

**Endpoints Used:**
- `/v1/news/all` - Financial news headlines

### 4. CoinMarketCap (Crypto - Optional)
**Purpose:** BTC, SOL prices
**Signup:** https://coinmarketcap.com/api/

## API Keys Storage

**⚠️ SECURITY WARNING:** Never commit API keys to GitHub!

**Recommended approach:**
```bash
# Create local config file (not tracked by git)
echo "TRADIER_TOKEN=your_token_here" > .env
echo "FINNHUB_TOKEN=your_token_here" >> .env

# Source in scripts
source .env
```

Add `.env` to `.gitignore` to prevent accidental commits.

## Testing APIs

Test each API after setup:

**Tradier:**
```bash
curl -X GET "https://sandbox.tradier.com/v1/markets/quotes?symbols=SPY" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Accept: application/json"
```

**Finnhub:**
```bash
curl "https://finnhub.io/api/v1/quote?symbol=SPY&token=YOUR_TOKEN"
```

## Troubleshooting

**401 Unauthorized:**
- Check token is correct
- Verify token hasn't expired
- Ensure proper header format

**Rate Limited:**
- Reduce API call frequency
- Add delays between requests
- Consider upgrading tier

**No Data Returned:**
- Check ticker symbol is valid
- Verify market is open
- Try different expiration dates

## Cost Considerations

| API | Free Tier | Paid Tier | Monthly Cost |
|-----|-----------|-----------|--------------|
| Tradier | Sandbox only | Live data | $0-49 |
| Finnhub | 60/min | Unlimited | $0-29 |
| Marketaux | Limited | Full access | $0-19 |

**Total monthly cost:** $0-97 depending on needs

## Next Steps

1. Sign up for all three APIs
2. Test each with sample requests
3. Store keys securely (not in repo)
4. Run `csp-scanner.sh` to verify

---

*Last Updated: March 2026*
