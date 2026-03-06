# Kelvin Capital Dashboard

A real-time web dashboard for monitoring the Kelvin Capital options trading bot.

## Features

- **Portfolio Overview**: Track capital, P&L, and returns
- **Position Monitoring**: Real-time status of open CSP positions
- **Trade Statistics**: Win rate, total trades, assignments
- **Market Snapshot**: Live prices for SPY, QQQ, BTC, SOL
- **Activity Feed**: Recent trades and market scans
- **Auto-refresh**: Updates every 60 seconds during market hours

## Usage

Open `index.html` in any modern web browser:

```bash
# From repository root
cd dashboard
open index.html  # macOS
# or
xdg-open index.html  # Linux
# or
start index.html  # Windows
```

Or serve with a simple HTTP server:

```bash
python -m http.server 8080
# Then visit http://localhost:8080
```

## Architecture

```
dashboard/
├── index.html      # Main dashboard UI
├── styles.css      # Dark theme styling
├── dashboard.js    # Interactive components
└── README.md       # This file
```

## Key Components

### Dashboard Class
Main controller handling:
- Timestamp updates
- Auto-refresh logic
- Data formatting utilities

### PositionManager
Position tracking:
- Add/close positions
- Real-time status updates
- Distance-to-strike calculations

### MarketDataService
Price data:
- API integration (placeholder)
- Caching layer
- Mock data for development

## Styling

Dark theme optimized for:
- Extended viewing sessions
- Reduced eye strain
- Professional trading environment

Colors:
- Background: #0a0a0f (deep black)
- Cards: #1a1a25 (dark gray)
- Accent: #10b981 (green for gains)
- Danger: #ef4444 (red for losses)

## Future Enhancements

- [ ] Real-time WebSocket data
- [ ] Interactive charts (Chart.js)
- [ ] P&L visualization over time
- [ ] Mobile app companion
- [ ] Alert notifications

## Screenshots

*Coming soon*

---

Part of Kelvin Capital - AI-powered options trading on Raspberry Pi 5
