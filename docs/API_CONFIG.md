# API Configuration

## Tradier API

### Setup Steps
1. Create account at https://developer.tradier.com/
2. Generate API token
3. Choose Sandbox (paper trading) or Production
4. Add token to environment or scripts

### Token Storage
```bash
# Option 1: Environment variable
export TRADIER_TOKEN="your_token_here"

# Option 2: Direct in script (less secure)
API_KEY="your_token_here"
```

### Rate Limits
- **Market Data:** 60 requests per minute
- **Order Placement:** 10 requests per minute
- **Account Data:** 60 requests per minute

### Endpoints Used
- `/markets/quotes` — Stock prices
- `/markets/options/expirations` — Available expirations
- `/markets/options/chains` — Option chains with Greeks
- `/markets/options/strikes` — Available strikes

---

## Finnhub API

### Setup Steps
1. Sign up at https://finnhub.io/
2. Get free API key
3. Add to scripts

### Free Tier Limits
- 60 API calls per minute
- Websocket access
- Delayed data (15 min)

### Endpoints Used
- `/api/v1/quote` — Real-time quotes
- `/api/v1/stock/profile2` — Company info
- `/api/v1/calendar/earnings` — Earnings dates

---

## Marketaux API

### Setup Steps
1. Register at https://www.marketaux.com/
2. Get API key
3. Configure in scripts

### Free Tier
- 100 requests per day
- Real-time news
- Filter by ticker, topic, or sentiment

### Usage
```bash
curl "https://api.marketaux.com/v1/news/all?symbols=TSLA&filter_entities=true&language=en&api_token=YOUR_TOKEN"
```

---

## Environment File Template

Create `.env` file:
```
TRADIER_TOKEN=your_tradier_token
FINNHUB_TOKEN=your_finnhub_token
MARKETAUX_TOKEN=your_marketaux_token
```

Load in scripts:
```bash
source .env
```

---

*Last updated: March 2026*
