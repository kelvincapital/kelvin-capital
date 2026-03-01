#!/bin/bash
# CSP Scanner for Kelvin Capital
# Scans UNIVERSE_50 for Wheel Strategy opportunities

API_KEY="WaIfCAGlCrHWwuw4BXmgL6bsyl5h"
BASE_URL="https://sandbox.tradier.com/v1"

# Universe of 50 sub-$200 S&P 500 tickers
UNIVERSE=(
"INTC" "CSCO" "IBM" "QCOM" "AMD" "MU" "HPQ" "HPE" "NXPI" "TXN"
"BAC" "WFC" "C" "USB" "PNC" "TFC" "COF" "BK" "AIG" "MET" "PRU"
"KO" "PEP" "WMT" "MCD" "SBUX" "LOW" "TGT" "DG" "KHC" "GIS" "CL"
"FDX" "UPS" "CAT" "DE" "HON" "EMR" "ETN" "DOV"
"PFE" "MRK" "ABBV" "BMY" "GILD" "CVS" "MDT" "AMGN" "SYK"
)

# Personal Watchlist (non-S&P, high conviction)
PERSONAL_WATCHLIST=(
"BULL"
)

echo "================================"
echo "KELVIN CAPITAL CSP SCANNER"
echo "Phase 1 - Sub-\$200 S&P 500"
echo "Tradier Sandbox API"
echo "================================"
echo ""
echo "Scanning ${#UNIVERSE[@]} S&P 500 tickers..."
echo "+ ${#PERSONAL_WATCHLIST[@]} personal watchlist tickers"
echo ""

# Temporary file for results
RESULTS_FILE=$(mktemp)

# Function to get stock price
get_price() {
    local ticker=$1
    curl -s -X GET "${BASE_URL}/markets/quotes?symbols=${ticker}" \
        -H "Authorization: Bearer ${API_KEY}" \
        -H "Accept: application/json" | grep -o '"last":[0-9.]*' | cut -d: -f2
}

# Function to get options expirations
get_expirations() {
    local ticker=$1
    curl -s -X GET "${BASE_URL}/markets/options/expirations?symbol=${ticker}" \
        -H "Authorization: Bearer ${API_KEY}" \
        -H "Accept: application/json" | grep -o '"date":"[^"]*"' | sed 's/"date":"//;s/"$//' | sort
}

# Function to get options chain
calculate_dte() {
    local exp_date=$1
    local today=$(date +%Y-%m-%d)
    local exp_epoch=$(date -d "$exp_date" +%s 2>/dev/null || echo "0")
    local today_epoch=$(date -d "$today" +%s)
    echo $(( (exp_epoch - today_epoch) / 86400 ))
}

# Main scanning loop
# Combine S&P 500 universe with personal watchlist
ALL_TICKERS=("${UNIVERSE[@]}" "${PERSONAL_WATCHLIST[@]}")

for ticker in "${ALL_TICKERS[@]}"; do
    echo -n "Scanning $ticker... "
    
    # Get current price
    price=$(get_price "$ticker")
    if [ -z "$price" ] || [ "$price" = "null" ]; then
        echo "SKIP (no price)"
        continue
    fi
    
    # Skip if price > $200 (S&P 500 universe only, personal watchlist exempt)
    if [[ " ${UNIVERSE[*]} " =~ " ${ticker} " ]] && (( $(echo "$price > 200" | bc -l) )); then
        echo "SKIP (price \$$price > \$200)"
        continue
    fi
    
    echo "Price: \$$price"
    
    # Get expirations
    expirations=$(get_expirations "$ticker")
    
    # Check each expiration for 7-14 DTE
    for exp in $expirations; do
        dte=$(calculate_dte "$exp")
        
        # Skip if not 7-14 DTE
        if [ "$dte" -lt 7 ] || [ "$dte" -gt 14 ]; then
            continue
        fi
        
        # Get options chain with Greeks
        chain=$(curl -s -X GET "${BASE_URL}/markets/options/chains?symbol=${ticker}&expiration=${exp}&greeks=true" \
            -H "Authorization: Bearer ${API_KEY}" \
            -H "Accept: application/json")
        
        # Process puts only
        echo "$chain" | grep -o '"option_type":"put"[^}]*' | while read -r put; do
            # Extract fields
            strike=$(echo "$put" | grep -o '"strike":[0-9.]*' | cut -d: -f2)
            bid=$(echo "$put" | grep -o '"bid":[0-9.]*' | cut -d: -f2)
            ask=$(echo "$put" | grep -o '"ask":[0-9.]*' | cut -d: -f2)
            oi=$(echo "$put" | grep -o '"open_interest":[0-9]*' | cut -d: -f2)
            delta=$(echo "$put" | grep -o '"delta":[0-9.-]*' | head -1 | cut -d: -f2)
            iv=$(echo "$put" | grep -o '"bid_iv":[0-9.]*' | cut -d: -f2)
            
            # Skip if missing data
            [ -z "$strike" ] || [ -z "$bid" ] || [ -z "$ask" ] && continue
            [ "$bid" = "0" ] || [ "$ask" = "0" ] && continue
            [ -z "$oi" ] && oi=0
            [ -z "$delta" ] && delta=0
            
            # Filter: OI >= 200
            if [ "$oi" -lt 200 ]; then
                continue
            fi
            
            # Filter: Delta 0.20-0.30
            delta_check=$(echo "$delta >= 0.20 && $delta <= 0.30" | bc -l)
            [ "$delta_check" -ne 1 ] && continue
            
            # Calculate spread %
            mid=$(echo "scale=2; ($bid + $ask) / 2" | bc -l)
            spread=$(echo "scale=2; ($ask - $bid)" | bc -l)
            spread_pct=$(echo "scale=2; ($spread / $mid) * 100" | bc -l)
            
            # Filter: Spread <= 20%
            spread_check=$(echo "$spread_pct <= 20" | bc -l)
            [ "$spread_check" -ne 1 ] && continue
            
            # Calculate Weekly ROC
            weekly_roc=$(echo "scale=4; ($mid / $strike) / ($dte / 7) * 100" | bc -l)
            
            # Filter: Weekly ROC >= 0.7%
            roc_check=$(echo "$weekly_roc >= 0.7" | bc -l)
            [ "$roc_check" -ne 1 ] && continue
            
            # Save result
            echo "$ticker,$strike,$exp,$dte,$mid,$delta,$iv,$oi,$spread_pct,$weekly_roc" >> "$RESULTS_FILE"
        done
    done
done

echo ""
echo "================================"
echo "SCAN COMPLETE"
echo "================================"
echo ""

# Sort by Weekly ROC (desc), then Spread % (asc), then OI (desc)
if [ -s "$RESULTS_FILE" ]; then
    echo "TOP 10 CSP CANDIDATES:"
    echo ""
    printf "%-6s %-8s %-12s %-4s %-10s %-6s %-6s %-8s %-8s %-10s\n" \
        "TICKER" "STRIKE" "EXPIRATION" "DTE" "MID" "DELTA" "IV" "OI" "SPREAD%" "WEEKLY ROC%"
    printf "%s\n" "--------------------------------------------------------------------------------------------------------"
    
    sort -t, -k10 -nr "$RESULTS_FILE" | head -10 | while IFS=, read -r ticker strike exp dte mid delta iv oi spread roc; do
        printf "%-6s $%-7.2f %-12s %-4s $%-9.2f %-6.2f %-6.2f %-8s %-8.2f %-10.4f\n" \
            "$ticker" "$strike" "$exp" "$dte" "$mid" "$delta" "$iv" "$oi" "$spread" "$roc"
    done
else
    echo "No qualifying CSP candidates found."
fi

# Print 3 random ticker quotes for verification
echo ""
echo "================================"
echo "PRICE VERIFICATION (3 Random)"
echo "================================"
echo ""

for i in 1 2 3; do
    random_ticker=${UNIVERSE[$RANDOM % ${#UNIVERSE[@]}]}
    echo "Ticker: $random_ticker"
    curl -s -X GET "${BASE_URL}/markets/quotes?symbols=${random_ticker}" \
        -H "Authorization: Bearer ${API_KEY}" \
        -H "Accept: application/json" | python3 -m json.tool 2>/dev/null || echo "Raw JSON:"
    echo ""
done

# Cleanup
rm -f "$RESULTS_FILE"
