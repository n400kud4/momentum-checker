# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a momentum-based ETF trading strategy backtesting application built with Python and Streamlit. The app analyzes momentum between TQQQ (3x leveraged NASDAQ ETF) and GLD (Gold ETF) to determine optimal holdings based on IEF (Treasury ETF) performance as a benchmark.

## Development Commands

### Environment Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the Application
```bash
# Main application (production)
source venv/bin/activate && streamlit run app.py

# Alternative test versions
streamlit run app_simple.py     # Simplified version with connection pooling
streamlit run test_app.py       # Minimal test version
streamlit run minimal_app.py    # Subprocess-based version

# Direct data testing (no UI)
python direct_test.py
```

### Streamlit Configuration
- Custom config at `.streamlit/config.toml` optimizes connection stability
- Default ports: 8505-8509 (configured to avoid conflicts)
- Connection error mitigation: CORS disabled, XSRF protection disabled

## Application Architecture

### Core Strategy Logic
The momentum strategy follows this decision tree:
1. **Data Collection**: Monthly open prices for IEF, TQQQ, GLD via yfinance
2. **Momentum Signal**: IEF 1-month return calculation: `(current_open - previous_open) / previous_open * 100`
3. **Position Selection**: Positive IEF return → TQQQ, Negative IEF return → GLD
4. **Rebalancing**: 3-month holding periods starting from user-defined start date
5. **Performance Calculation**: Simple return formula for each 3-month period

### Key Technical Implementation

**Data Handling**:
- `@st.cache_data(ttl=600)` caching prevents excessive API calls
- Timezone normalization via `tz_localize(None)` prevents comparison errors
- Sequential data fetching with 1-2 second delays to avoid rate limiting

**Connection Stability**:
- Multiple app versions handle different levels of connection issues
- `direct_test.py` provides fallback for pure data verification
- Custom requests session with retry logic in advanced versions

**File Structure**:
- `app.py`: Main production application with full UI
- `app_simple.py`: Connection-optimized version with progress indicators  
- `direct_test.py`: Standalone data testing script
- `requirements.txt`: Production dependencies (streamlit, yfinance, pandas, numpy, plotly)

### Data Requirements
- **TQQQ**: March 2010 onwards
- **GLD/IEF**: 2004 onwards  
- **Default period**: January 2015 to present
- **Pricing**: Monthly open prices only (not adjusted close)
- **Interval**: Monthly data (`interval="1mo"` in yfinance)

### Known Issues & Solutions
- **yfinance connection errors**: Resolved with retry logic and request session management
- **Timezone comparison errors**: Fixed with timezone normalization in data preprocessing
- **Streamlit connection drops**: Mitigated with custom server configuration and multiple app variants