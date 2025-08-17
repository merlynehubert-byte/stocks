import streamlit as st

# Page configuration must be the first Streamlit command
st.set_page_config(
    page_title="Advanced Stock Trading Education Hub",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import requests
import json

# Try to import scipy, fallback if not available
try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    st.warning("SciPy not available. Some advanced features may be limited.")

# Try to import TA-Lib, fallback to manual implementation if not available
try:
    import talib
    TALIB_AVAILABLE = True
except ImportError:
    TALIB_AVAILABLE = False
    st.warning("TA-Lib not available. Using simplified technical indicators.")

# Custom CSS for advanced styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .section-header {
        font-size: 2rem;
        color: #2e8b57;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #2e8b57;
        padding-bottom: 0.5rem;
    }
    .subsection-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .info-box {
        background: linear-gradient(135deg, #f0f2f6 0%, #e8f4fd 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .example-box {
        background: linear-gradient(135deg, #e8f4fd 0%, #d1ecf1 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        border-left: 5px solid #17a2b8;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 0.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .ai-analysis-box {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 4rem;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 0.5rem 0.5rem 0rem 0rem;
        gap: 1rem;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {}
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []
if 'learning_progress' not in st.session_state:
    st.session_state.learning_progress = {}

# Manual technical indicators implementation (fallback)
def calculate_rsi(prices, period=14):
    """Calculate RSI manually"""
    deltas = np.diff(prices)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    
    avg_gains = pd.Series(gains).rolling(window=period).mean()
    avg_losses = pd.Series(losses).rolling(window=period).mean()
    
    rs = avg_gains / avg_losses
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_sma(prices, period):
    """Calculate Simple Moving Average"""
    return pd.Series(prices).rolling(window=period).mean()

def calculate_ema(prices, period):
    """Calculate Exponential Moving Average"""
    return pd.Series(prices).ewm(span=period).mean()

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calculate MACD manually"""
    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)
    macd_line = ema_fast - ema_slow
    signal_line = calculate_ema(macd_line, signal)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def calculate_bollinger_bands(prices, period=20, std_dev=2):
    """Calculate Bollinger Bands"""
    sma = calculate_sma(prices, period)
    std = pd.Series(prices).rolling(window=period).std()
    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)
    return upper_band, sma, lower_band

def calculate_stochastic(high, low, close, k_period=14, d_period=3):
    """Calculate Stochastic Oscillator"""
    lowest_low = pd.Series(low).rolling(window=k_period).min()
    highest_high = pd.Series(high).rolling(window=k_period).max()
    
    k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
    d_percent = calculate_sma(k_percent, d_period)
    
    return k_percent, d_percent

def calculate_obv(close, volume):
    """Calculate On-Balance Volume"""
    obv = [0]
    for i in range(1, len(close)):
        if close[i] > close[i-1]:
            obv.append(obv[-1] + volume[i])
        elif close[i] < close[i-1]:
            obv.append(obv[-1] - volume[i])
        else:
            obv.append(obv[-1])
    return pd.Series(obv)

# Real-time stock data function
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_stock_data(symbol, period="1y"):
    try:
        # Clean the symbol
        symbol = symbol.strip().upper()
        
        # Create ticker object
        stock = yf.Ticker(symbol)
        
        # Get historical data with better error handling
        try:
            hist = stock.history(period=period, progress=False)
            if hist.empty:
                st.error(f"No data found for {symbol}. Please check the symbol.")
                return None, None
        except Exception as e:
            st.error(f"Error fetching historical data for {symbol}: {str(e)}")
            return None, None
        
        # Get stock info with error handling
        try:
            info = stock.info
            if not info or len(info) < 5:  # Basic validation
                info = {}
        except Exception as e:
            st.warning(f"Could not fetch detailed info for {symbol}: {str(e)}")
            info = {}
        
        return hist, info
    except Exception as e:
        st.error(f"Error with {symbol}: {str(e)}")
        return None, None

# Technical indicators calculation
def calculate_technical_indicators(df):
    if df is None or df.empty:
        return df
    
    # Ensure we have the required columns
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    if not all(col in df.columns for col in required_columns):
        st.error("Missing required price data columns")
        return df
    
    # Check if we have enough data points
    if len(df) < 50:
        st.warning(f"Limited data points ({len(df)}). Some indicators may not be accurate.")
    
    try:
        prices = df['Close'].values
        high = df['High'].values
        low = df['Low'].values
        volume = df['Volume'].values
        
        if TALIB_AVAILABLE:
            # Use TA-Lib if available
            df['RSI'] = talib.RSI(prices, timeperiod=14)
            df['SMA_20'] = talib.SMA(prices, timeperiod=20)
            df['SMA_50'] = talib.SMA(prices, timeperiod=50)
            df['EMA_12'] = talib.EMA(prices, timeperiod=12)
            df['EMA_26'] = talib.EMA(prices, timeperiod=26)
            df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = talib.MACD(prices)
            df['BB_Upper'], df['BB_Middle'], df['BB_Lower'] = talib.BBANDS(prices)
            df['STOCH_K'], df['STOCH_D'] = talib.STOCH(high, low, prices)
            df['OBV'] = talib.OBV(prices, volume)
        else:
            # Use manual implementation
            df['RSI'] = calculate_rsi(prices, 14)
            df['SMA_20'] = calculate_sma(prices, 20)
            df['SMA_50'] = calculate_sma(prices, 50)
            df['EMA_12'] = calculate_ema(prices, 12)
            df['EMA_26'] = calculate_ema(prices, 26)
            df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = calculate_macd(prices)
            df['BB_Upper'], df['BB_Middle'], df['BB_Lower'] = calculate_bollinger_bands(prices)
            df['STOCH_K'], df['STOCH_D'] = calculate_stochastic(high, low, prices)
            df['OBV'] = calculate_obv(prices, volume)
        
        return df
    except Exception as e:
        st.error(f"Error calculating technical indicators: {str(e)}")
        return df

# AI-powered analysis function
def ai_analysis(df, symbol):
    if df is None or df.empty:
        return "Insufficient data for analysis"
    
    signals = []
    
    # RSI Analysis
    if 'RSI' in df.columns and not df['RSI'].isna().all():
        current_rsi = df['RSI'].iloc[-1]
        if not pd.isna(current_rsi):
            if current_rsi > 70:
                signals.append("RSI indicates overbought conditions (>70)")
            elif current_rsi < 30:
                signals.append("RSI indicates oversold conditions (<30)")
            else:
                signals.append(f"RSI is neutral at {current_rsi:.1f}")
    
    # Moving Average Analysis
    current_price = df['Close'].iloc[-1]
    if 'SMA_20' in df.columns and 'SMA_50' in df.columns:
        sma_20 = df['SMA_20'].iloc[-1]
        sma_50 = df['SMA_50'].iloc[-1]
        
        if not pd.isna(sma_20) and not pd.isna(sma_50):
            if current_price > sma_20 > sma_50:
                signals.append("Strong uptrend: Price above 20-day and 50-day SMAs")
            elif current_price < sma_20 < sma_50:
                signals.append("Strong downtrend: Price below 20-day and 50-day SMAs")
            elif current_price > sma_20 and sma_20 < sma_50:
                signals.append("Potential trend reversal: Price above 20-day SMA but below 50-day SMA")
    
    # MACD Analysis
    if 'MACD' in df.columns and 'MACD_Signal' in df.columns:
        macd = df['MACD'].iloc[-1]
        macd_signal = df['MACD_Signal'].iloc[-1]
        
        if not pd.isna(macd) and not pd.isna(macd_signal):
            if macd > macd_signal:
                signals.append("MACD bullish: MACD line above signal line")
            else:
                signals.append("MACD bearish: MACD line below signal line")
    
    # Bollinger Bands Analysis
    if 'BB_Upper' in df.columns and 'BB_Lower' in df.columns:
        bb_upper = df['BB_Upper'].iloc[-1]
        bb_lower = df['BB_Lower'].iloc[-1]
        
        if not pd.isna(bb_upper) and not pd.isna(bb_lower):
            if current_price > bb_upper:
                signals.append("Price above upper Bollinger Band - potential reversal")
            elif current_price < bb_lower:
                signals.append("Price below lower Bollinger Band - potential bounce")
            else:
                signals.append("Price within Bollinger Bands - normal volatility")
    
    # Volume Analysis
    avg_volume = df['Volume'].rolling(20).mean().iloc[-1]
    current_volume = df['Volume'].iloc[-1]
    
    if current_volume > avg_volume * 1.5:
        signals.append("High volume - strong conviction in current move")
    elif current_volume < avg_volume * 0.5:
        signals.append("Low volume - weak conviction in current move")
    
    return signals

# Sidebar navigation
st.sidebar.title("📚 Advanced Learning Hub")
page = st.sidebar.selectbox(
    "Choose a module:",
    [
        "🏠 Dashboard",
        "📊 Real-Time Analysis",
        "🎯 Options Masterclass",
        "📈 Technical Analysis",
        "💰 Strategy Builder",
        "📋 Portfolio Simulator",
        "🤖 AI Insights",
        "📚 Learning Path",
        "🎮 Interactive Tools"
    ]
)

# Dashboard
if page == "🏠 Dashboard":
    st.markdown('<h1 class="main-header">📈 Advanced Stock Trading Education Hub</h1>', unsafe_allow_html=True)
    
    # Market overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">📊</div>
            <div class="metric-label">Real-Time Data</div>
            <div class="metric-label">Live Market Analysis</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">🤖</div>
            <div class="metric-label">AI Analysis</div>
            <div class="metric-label">Smart Insights</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">📈</div>
            <div class="metric-label">Advanced Charts</div>
            <div class="metric-label">Technical Indicators</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">💰</div>
            <div class="metric-label">Portfolio Sim</div>
            <div class="metric-label">Risk-Free Trading</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick stock lookup
    st.markdown('<h2 class="subsection-header">🔍 Quick Stock Analysis</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        symbol = st.text_input("Enter stock symbol:", value="AAPL").upper()
    
    with col2:
        if st.button("Analyze"):
            if symbol:
                with st.spinner("Fetching data..."):
                    hist, info = get_stock_data(symbol)
                    if hist is not None and not hist.empty:
                        st.session_state.current_stock = {
                            'symbol': symbol,
                            'data': hist,
                            'info': info
                        }
                        st.success(f"✅ {symbol} data loaded successfully!")
                    else:
                        st.error(f"❌ Could not fetch data for {symbol}")

# Real-Time Analysis
elif page == "📊 Real-Time Analysis":
    st.markdown('<h1 class="section-header">📊 Real-Time Market Analysis</h1>', unsafe_allow_html=True)
    
    if 'current_stock' in st.session_state:
        symbol = st.session_state.current_stock['symbol']
        df = st.session_state.current_stock['data']
        info = st.session_state.current_stock['info']
        
        # Calculate technical indicators
        df = calculate_technical_indicators(df)
        
        # Stock overview
        col1, col2, col3, col4 = st.columns(4)
        
        current_price = df['Close'].iloc[-1]
        price_change = df['Close'].iloc[-1] - df['Close'].iloc[-2]
        price_change_pct = (price_change / df['Close'].iloc[-2]) * 100
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">${current_price:.2f}</div>
                <div class="metric-label">{symbol}</div>
                <div class="metric-label">{price_change:+.2f} ({price_change_pct:+.2f}%)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if info and 'marketCap' in info:
                market_cap = info['marketCap'] / 1e9  # Convert to billions
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">${market_cap:.1f}B</div>
                    <div class="metric-label">Market Cap</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col3:
            if info and 'trailingPE' in info:
                pe_ratio = info['trailingPE']
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{pe_ratio:.1f}</div>
                    <div class="metric-label">P/E Ratio</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col4:
            if info and 'dividendYield' in info:
                dividend_yield = info['dividendYield'] * 100 if info['dividendYield'] else 0
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{dividend_yield:.2f}%</div>
                    <div class="metric-label">Dividend Yield</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Advanced chart
        st.markdown('<h3 class="subsection-header">📈 Advanced Technical Chart</h3>', unsafe_allow_html=True)
        
        fig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=('Price & Moving Averages', 'RSI', 'MACD', 'Volume'),
            row_heights=[0.5, 0.2, 0.2, 0.1]
        )
        
        # Price and moving averages
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Price'
        ), row=1, col=1)
        
        if 'SMA_20' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], name='SMA 20', line=dict(color='orange')), row=1, col=1)
        if 'SMA_50' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], name='SMA 50', line=dict(color='red')), row=1, col=1)
        
        # RSI
        if 'RSI' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color='purple')), row=2, col=1)
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
        
        # MACD
        if 'MACD' in df.columns and 'MACD_Signal' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='blue')), row=3, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], name='Signal', line=dict(color='red')), row=3, col=1)
            if 'MACD_Hist' in df.columns:
                fig.add_trace(go.Bar(x=df.index, y=df['MACD_Hist'], name='Histogram'), row=3, col=1)
        
        # Volume
        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume'), row=4, col=1)
        
        fig.update_layout(height=800, title_text=f"{symbol} Technical Analysis")
        st.plotly_chart(fig, use_container_width=True)
        
        # AI Analysis
        st.markdown('<h3 class="subsection-header">🤖 AI-Powered Analysis</h3>', unsafe_allow_html=True)
        
        signals = ai_analysis(df, symbol)
        
        st.markdown("""
        <div class="ai-analysis-box">
            <h4>🎯 Trading Signals & Insights</h4>
        </div>
        """, unsafe_allow_html=True)
        
        for signal in signals:
            st.markdown(f"• {signal}")
    
    else:
        st.info("Please load a stock from the Dashboard first!")

# Options Masterclass
elif page == "🎯 Options Masterclass":
    st.markdown('<h1 class="section-header">🎯 Advanced Options Trading</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📞 Call Strategies", "📞 Put Strategies", "🎯 Advanced Strategies", "💰 Risk Management"])
    
    with tab1:
        st.markdown('<h3 class="subsection-header">📞 Call Option Strategies</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="example-box">
                <h4>📈 Long Call Strategy</h4>
                <p><strong>When to use:</strong> Bullish on stock, expect significant upside</p>
                <p><strong>Risk:</strong> Limited to premium paid</p>
                <p><strong>Reward:</strong> Unlimited upside potential</p>
                <p><strong>Break-even:</strong> Strike price + premium</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="example-box">
                <h4>📉 Covered Call Strategy</h4>
                <p><strong>When to use:</strong> Own stock, expect sideways movement</p>
                <p><strong>Risk:</strong> Limited upside if stock rises significantly</p>
                <p><strong>Reward:</strong> Premium income + stock appreciation up to strike</p>
                <p><strong>Break-even:</strong> Stock purchase price - premium</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<h3 class="subsection-header">📞 Put Option Strategies</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="example-box">
                <h4>📉 Long Put Strategy</h4>
                <p><strong>When to use:</strong> Bearish on stock, expect significant downside</p>
                <p><strong>Risk:</strong> Limited to premium paid</p>
                <p><strong>Reward:</strong> Profit if stock falls below strike - premium</p>
                <p><strong>Break-even:</strong> Strike price - premium</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="example-box">
                <h4>💰 Cash Secured Put</h4>
                <p><strong>When to use:</strong> Want to buy stock at lower price</p>
                <p><strong>Risk:</strong> Must buy stock if assigned</p>
                <p><strong>Reward:</strong> Premium income + potential stock acquisition</p>
                <p><strong>Break-even:</strong> Strike price - premium</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<h3 class="subsection-header">🎯 Advanced Options Strategies</h3>', unsafe_allow_html=True)
        
        strategies = {
            "Iron Condor": {
                "description": "Sell both calls and puts for income",
                "setup": "Sell OTM call + sell OTM put",
                "profit": "Premium collected",
                "risk": "Unlimited if stock moves beyond strikes"
            },
            "Butterfly Spread": {
                "description": "Limited risk, limited reward strategy",
                "setup": "Buy 1 call + sell 2 calls + buy 1 call",
                "profit": "Maximum at middle strike",
                "risk": "Limited to net premium paid"
            },
            "Straddle": {
                "description": "Profit from large price movement",
                "setup": "Buy call + buy put at same strike",
                "profit": "Unlimited in either direction",
                "risk": "Premium paid for both options"
            }
        }
        
        for strategy, details in strategies.items():
            with st.expander(f"🎯 {strategy}"):
                st.markdown(f"**Description:** {details['description']}")
                st.markdown(f"**Setup:** {details['setup']}")
                st.markdown(f"**Profit Potential:** {details['profit']}")
                st.markdown(f"**Risk:** {details['risk']}")

# Portfolio Simulator
elif page == "📋 Portfolio Simulator":
    st.markdown('<h1 class="section-header">📋 Portfolio Simulator</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["💰 Portfolio Builder", "📊 Performance Analysis", "🎯 Risk Management"])
    
    with tab1:
        st.markdown('<h3 class="subsection-header">💰 Build Your Portfolio</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            symbol = st.text_input("Stock Symbol:", value="AAPL").upper()
            shares = st.number_input("Number of Shares:", min_value=1, value=100)
            price = st.number_input("Purchase Price:", min_value=0.01, value=150.0)
            
            if st.button("Add to Portfolio"):
                if symbol and shares and price:
                    if symbol not in st.session_state.portfolio:
                        st.session_state.portfolio[symbol] = {
                            'shares': shares,
                            'avg_price': price,
                            'total_cost': shares * price
                        }
                    else:
                        # Update existing position
                        current = st.session_state.portfolio[symbol]
                        total_shares = current['shares'] + shares
                        total_cost = current['total_cost'] + (shares * price)
                        st.session_state.portfolio[symbol] = {
                            'shares': total_shares,
                            'avg_price': total_cost / total_shares,
                            'total_cost': total_cost
                        }
                    st.success(f"✅ Added {shares} shares of {symbol} to portfolio!")
        
        with col2:
            st.markdown("**Current Portfolio:**")
            if st.session_state.portfolio:
                for symbol, position in st.session_state.portfolio.items():
                    st.markdown(f"""
                    **{symbol}**: {position['shares']} shares @ ${position['avg_price']:.2f}
                    Total Cost: ${position['total_cost']:,.2f}
                    """)
            else:
                st.info("No positions in portfolio yet.")
    
    with tab2:
        st.markdown('<h3 class="subsection-header">📊 Portfolio Performance</h3>', unsafe_allow_html=True)
        
        if st.session_state.portfolio:
            # Calculate current values
            portfolio_data = []
            total_current_value = 0
            total_cost = 0
            
            for symbol, position in st.session_state.portfolio.items():
                hist, info = get_stock_data(symbol, "1d")
                if hist is not None and not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    current_value = position['shares'] * current_price
                    gain_loss = current_value - position['total_cost']
                    gain_loss_pct = (gain_loss / position['total_cost']) * 100
                    
                    portfolio_data.append({
                        'Symbol': symbol,
                        'Shares': position['shares'],
                        'Avg Price': position['avg_price'],
                        'Current Price': current_price,
                        'Total Cost': position['total_cost'],
                        'Current Value': current_value,
                        'Gain/Loss': gain_loss,
                        'Gain/Loss %': gain_loss_pct
                    })
                    
                    total_current_value += current_value
                    total_cost += position['total_cost']
            
            if portfolio_data:
                df_portfolio = pd.DataFrame(portfolio_data)
                st.dataframe(df_portfolio, use_container_width=True)
                
                total_gain_loss = total_current_value - total_cost
                total_gain_loss_pct = (total_gain_loss / total_cost) * 100
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Cost", f"${total_cost:,.2f}")
                with col2:
                    st.metric("Current Value", f"${total_current_value:,.2f}")
                with col3:
                    st.metric("Total P&L", f"${total_gain_loss:,.2f}", f"{total_gain_loss_pct:+.2f}%")
        else:
            st.info("No positions to analyze. Add some stocks to your portfolio first!")

# Interactive Tools
elif page == "🎮 Interactive Tools":
    st.markdown('<h1 class="section-header">🎮 Interactive Learning Tools</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["💰 Options Calculator", "📊 Risk Calculator", "🎯 Strategy Tester", "📚 Knowledge Quiz"])
    
    with tab1:
        st.markdown('<h3 class="subsection-header">💰 Advanced Options Calculator</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            option_type = st.selectbox("Option Type", ["Call", "Put"])
            action = st.selectbox("Action", ["Buy", "Sell"])
            strike_price = st.number_input("Strike Price ($)", min_value=1.0, value=50.0, step=1.0)
            premium = st.number_input("Premium ($)", min_value=0.01, value=2.0, step=0.01)
            expiration_days = st.number_input("Days to Expiration", min_value=1, value=30, step=1)
        
        with col2:
            current_price = st.number_input("Current Stock Price ($)", min_value=1.0, value=50.0, step=1.0)
            shares_per_contract = st.number_input("Shares per Contract", min_value=1, value=100, step=1)
            volatility = st.slider("Implied Volatility (%)", min_value=10, max_value=200, value=30, step=5)
        
        # Calculate profit/loss at different price points
        price_range = np.linspace(current_price * 0.7, current_price * 1.3, 50)
        profits = []
        
        for price in price_range:
            if option_type == "Call":
                if action == "Buy":
                    if price > strike_price:
                        intrinsic_value = price - strike_price
                        profit = (intrinsic_value - premium) * shares_per_contract
                    else:
                        profit = -premium * shares_per_contract
                else:  # Sell
                    if price > strike_price:
                        intrinsic_value = price - strike_price
                        profit = (premium - intrinsic_value) * shares_per_contract
                    else:
                        profit = premium * shares_per_contract
            else:  # Put
                if action == "Buy":
                    if price < strike_price:
                        intrinsic_value = strike_price - price
                        profit = (intrinsic_value - premium) * shares_per_contract
                    else:
                        profit = -premium * shares_per_contract
                else:  # Sell
                    if price < strike_price:
                        intrinsic_value = strike_price - price
                        profit = (premium - intrinsic_value) * shares_per_contract
                    else:
                        profit = premium * shares_per_contract
            
            profits.append(profit)
        
        # Plot profit/loss diagram
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=price_range, y=profits, mode='lines', name='Profit/Loss'))
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        fig.add_vline(x=strike_price, line_dash="dash", line_color="green", annotation_text="Strike Price")
        fig.add_vline(x=current_price, line_dash="dash", line_color="blue", annotation_text="Current Price")
        
        fig.update_layout(
            title=f"{action} {option_type} Option Profit/Loss Diagram",
            xaxis_title="Stock Price ($)",
            yaxis_title="Profit/Loss ($)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Current profit/loss
        current_profit = profits[len(price_range)//2]  # Profit at current price
        st.metric("Current Profit/Loss", f"${current_profit:.2f}")
    
    with tab2:
        st.markdown('<h3 class="subsection-header">📊 Advanced Risk Calculator</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            portfolio_value = st.number_input("Portfolio Value ($)", min_value=1000, value=10000, step=1000)
            risk_per_trade = st.slider("Risk per Trade (%)", min_value=0.5, max_value=5.0, value=1.0, step=0.1)
            stop_loss_pct = st.slider("Stop Loss (%)", min_value=1.0, max_value=20.0, value=5.0, step=0.5)
            max_positions = st.number_input("Maximum Concurrent Positions", min_value=1, value=5, step=1)
        
        with col2:
            risk_amount = portfolio_value * (risk_per_trade / 100)
            position_size = risk_amount / (stop_loss_pct / 100)
            max_portfolio_risk = risk_amount * max_positions
            portfolio_risk_pct = (max_portfolio_risk / portfolio_value) * 100
            
            st.markdown(f"""
            <div class="info-box">
                <h4>📊 Risk Analysis Results</h4>
                <p><strong>Risk per Trade:</strong> ${risk_amount:.2f} ({risk_per_trade}%)</p>
                <p><strong>Position Size:</strong> ${position_size:.2f}</p>
                <p><strong>Max Portfolio Risk:</strong> ${max_portfolio_risk:.2f} ({portfolio_risk_pct:.1f}%)</p>
                <p><strong>Stop Loss:</strong> {stop_loss_pct}%</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<h3 class="subsection-header">🎯 Strategy Tester</h3>', unsafe_allow_html=True)
        
        strategy = st.selectbox("Choose Strategy to Test:", [
            "Moving Average Crossover",
            "RSI Mean Reversion",
            "MACD Momentum",
            "Bollinger Bands Bounce",
            "Volume Breakout"
        ])
        
        if st.button("Run Backtest"):
            st.info("Backtesting feature coming soon! This will simulate trading strategies on historical data.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>📚 Educational content only. Always do your own research and consider consulting with financial advisors.</p>
    <p>Built with ❤️ using Streamlit | Real-time data from Yahoo Finance | AI-powered analysis</p>
</div>
""", unsafe_allow_html=True) 