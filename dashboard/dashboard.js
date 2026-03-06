/**
 * Kelvin Capital Dashboard
 * Real-time portfolio tracking and visualization
 */

class Dashboard {
    constructor() {
        this.refreshInterval = 60000; // 60 seconds
        this.init();
    }

    init() {
        this.updateTimestamp();
        this.startAutoRefresh();
        this.setupEventListeners();
    }

    /**
     * Update the last updated timestamp
     */
    updateTimestamp() {
        const now = new Date();
        const formatted = now.toLocaleString('en-US', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
        }) + ' EST';
        
        const element = document.getElementById('last-updated');
        if (element) {
            element.textContent = formatted;
        }
    }

    /**
     * Calculate days to expiration
     */
    calculateDTE(expirationDate) {
        const exp = new Date(expirationDate);
        const now = new Date();
        const diffTime = exp - now;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        return Math.max(0, diffDays);
    }

    /**
     * Format currency
     */
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2
        }).format(amount);
    }

    /**
     * Format percentage
     */
    formatPercent(value) {
        const sign = value >= 0 ? '+' : '';
        return `${sign}${value.toFixed(2)}%`;
    }

    /**
     * Update portfolio metrics
     */
    updateMetrics(data) {
        const pnl = data.pnl || 0;
        const pnlElement = document.getElementById('total-pnl');
        const returnElement = document.getElementById('total-return');
        
        if (pnlElement) {
            pnlElement.textContent = this.formatCurrency(pnl);
            pnlElement.className = `metric-value ${pnl >= 0 ? 'positive' : 'negative'}`;
        }
        
        if (returnElement) {
            const ret = (pnl / 30000) * 100;
            returnElement.textContent = this.formatPercent(ret);
            returnElement.className = `metric-value ${ret >= 0 ? 'positive' : 'negative'}`;
        }
    }

    /**
     * Check if market is open
     */
    isMarketOpen() {
        const now = new Date();
        const hour = now.getHours();
        const day = now.getDay();
        
        // Market hours: 9:30 AM - 4:00 PM EST, weekdays only
        return day >= 1 && day <= 5 && hour >= 9 && hour < 16;
    }

    /**
     * Start auto-refresh timer
     */
    startAutoRefresh() {
        setInterval(() => {
            this.updateTimestamp();
            
            // Only refresh data during market hours
            if (this.isMarketOpen()) {
                this.refreshData();
            }
        }, this.refreshInterval);
    }

    /**
     * Refresh dashboard data
     */
    async refreshData() {
        console.log('Refreshing dashboard data...');
        this.updateTimestamp();
        
        // In a real implementation, this would fetch from an API
        // For now, we just update the timestamp
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // 'R' to refresh
            if (e.key === 'r' && e.ctrlKey) {
                e.preventDefault();
                this.refreshData();
            }
        });
    }
}

/**
 * Position Manager
 * Handles position tracking and status updates
 */
class PositionManager {
    constructor() {
        this.positions = [];
    }

    /**
     * Add a new position
     */
    addPosition(position) {
        this.positions.push({
            ...position,
            openedAt: new Date(),
            status: 'open'
        });
        this.render();
    }

    /**
     * Update position status
     */
    updatePosition(ticker, updates) {
        const position = this.positions.find(p => p.ticker === ticker);
        if (position) {
            Object.assign(position, updates);
            this.render();
        }
    }

    /**
     * Close a position
     */
    closePosition(ticker, pnl) {
        const position = this.positions.find(p => p.ticker === ticker);
        if (position) {
            position.status = 'closed';
            position.closedAt = new Date();
            position.pnl = pnl;
            this.render();
        }
    }

    /**
     * Render positions to DOM
     */
    render() {
        const container = document.querySelector('.position-list');
        if (!container) return;

        // Clear current positions
        container.innerHTML = '';

        // Render each position
        this.positions.forEach(pos => {
            const card = this.createPositionCard(pos);
            container.appendChild(card);
        });
    }

    /**
     * Create position card element
     */
    createPositionCard(position) {
        const card = document.createElement('div');
        card.className = 'position-card';
        
        const isSafe = position.currentPrice > position.strike;
        const buffer = position.currentPrice - position.strike;
        const bufferPct = (buffer / position.currentPrice) * 100;
        
        card.innerHTML = `
            <div class="position-header">
                <span class="ticker">${position.ticker}</span>
                <span class="position-type">${position.type}</span>
            </div>
            <div class="position-details">
                <div class="detail">
                    <span class="detail-label">Strike</span>
                    <span class="detail-value">$${position.strike.toFixed(2)}</span>
                </div>
                <div class="detail">
                    <span class="detail-label">Current</span>
                    <span class="detail-value">$${position.currentPrice.toFixed(2)}</span>
                </div>
                <div class="detail">
                    <span class="detail-label">Buffer</span>
                    <span class="detail-value positive">$${buffer.toFixed(2)} (${bufferPct.toFixed(1)}%)</span>
                </div>
                <div class="detail">
                    <span class="detail-label">Expiration</span>
                    <span class="detail-value">${position.expiration}</span>
                </div>
            </div>
            <div class="position-status ${isSafe ? 'safe' : 'warning'}">
                <span class="status-icon">${isSafe ? '✓' : '⚠'}</span>
                <span>${isSafe ? 'Safe - Above Strike' : 'Warning - Monitor Closely'}</span>
            </div>
        `;
        
        return card;
    }
}

/**
 * Market Data Service
 * Fetches and caches market data
 */
class MarketDataService {
    constructor() {
        this.cache = new Map();
        this.cacheDuration = 60000; // 60 seconds
    }

    /**
     * Fetch price data
     */
    async getPrice(symbol) {
        const cached = this.cache.get(symbol);
        if (cached && Date.now() - cached.timestamp < this.cacheDuration) {
            return cached.data;
        }

        try {
            // In production, this would call your API
            // For now, return mock data
            const data = await this.fetchMockData(symbol);
            this.cache.set(symbol, {
                data,
                timestamp: Date.now()
            });
            return data;
        } catch (error) {
            console.error(`Error fetching ${symbol}:`, error);
            return null;
        }
    }

    /**
     * Mock data for development
     */
    async fetchMockData(symbol) {
        // Return realistic mock data
        const mockPrices = {
            'SPY': 681.31,
            'QQQ': 607.72,
            'WFC': 82.11,
            'BTC': 70765,
            'SOL': 90.27
        };

        return {
            symbol,
            price: mockPrices[symbol] || 100,
            change: (Math.random() - 0.5) * 2,
            timestamp: new Date().toISOString()
        };
    }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new Dashboard();
    window.positionManager = new PositionManager();
    window.marketData = new MarketDataService();
    
    console.log('Kelvin Capital Dashboard initialized');
});

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Dashboard, PositionManager, MarketDataService };
}
