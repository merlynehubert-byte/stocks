import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import requests
import json
import time
from typing import Dict, List, Optional, Tuple

# Page configuration
st.set_page_config(
    page_title="🚀 Advanced Stock Trading Education Hub",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for modern UI
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 2.5rem;
        color: #2e8b57;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        border-bottom: 3px solid #2e8b57;
        padding-bottom: 0.5rem;
    }
    .subsection-header {
        font-size: 1.8rem;
        color: #ff7f0e;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
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
    .ai-box {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
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
    .progress-bar {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 8px;
        border-radius: 4px;
        margin: 0.5rem 0;
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
if 'current_stock' not in st.session_state:
    st.session_state.current_stock = None

# Enhanced data fetching with better error handling
@st.cache_data(ttl=300)
def get_stock_data(symbol: str, period: str = "1y") -> Tuple[Optional[pd.DataFrame], Optional[Dict]]:
    """Enhanced stock data fetching with better error handling"""
    try:
        symbol = symbol.strip().upper()
        stock = yf.Ticker(symbol)
        
        # Get historical data
        hist = stock.history(period=period, progress=False)
        if hist.empty:
            return None, None
        
        # Get stock info
        info = stock.info
        if not info or len(info) < 5:
            info = {}
        
        return hist, info
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {str(e)}")
        return None, None

# Enhanced technical indicators
def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate comprehensive technical indicators"""
    if df is None or df.empty:
        return df
    
    try:
        prices = df['Close'].values
        high = df['High'].values
        low = df['Low'].values
        volume = df['Volume'].values
        
        # Moving Averages
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['EMA_12'] = df['Close'].ewm(span=12).mean()
        df['EMA_26'] = df['Close'].ewm(span=26).mean()
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
        df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
        
        # Bollinger Bands
        df['BB_Middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        # Volume indicators
        df['Volume_SMA'] = df['Volume'].rolling(window=20).mean()
        df['Volume_Ratio'] = df['Volume'] / df['Volume_SMA']
        
        return df
    except Exception as e:
        st.error(f"Error calculating indicators: {str(e)}")
        return df

# AI-powered analysis
def ai_analysis(df: pd.DataFrame, symbol: str) -> List[str]:
    """Enhanced AI analysis with multiple signals"""
    signals = []
    
    try:
        current_price = df['Close'].iloc[-1]
        
        # RSI Analysis
        if 'RSI' in df.columns:
            current_rsi = df['RSI'].iloc[-1]
            if not pd.isna(current_rsi):
                if current_rsi > 70:
                    signals.append(f"🔴 RSI overbought ({current_rsi:.1f}) - potential reversal")
                elif current_rsi < 30:
                    signals.append(f"🟢 RSI oversold ({current_rsi:.1f}) - potential bounce")
                else:
                    signals.append(f"🟡 RSI neutral ({current_rsi:.1f})")
        
        # Moving Average Analysis
        if 'SMA_20' in df.columns and 'SMA_50' in df.columns:
            sma_20 = df['SMA_20'].iloc[-1]
            sma_50 = df['SMA_50'].iloc[-1]
            
            if not pd.isna(sma_20) and not pd.isna(sma_50):
                if current_price > sma_20 > sma_50:
                    signals.append("📈 Strong uptrend - price above both SMAs")
                elif current_price < sma_20 < sma_50:
                    signals.append("📉 Strong downtrend - price below both SMAs")
                elif current_price > sma_20 and sma_20 < sma_50:
                    signals.append("🔄 Potential trend reversal")
        
        # MACD Analysis
        if 'MACD' in df.columns and 'MACD_Signal' in df.columns:
            macd = df['MACD'].iloc[-1]
            macd_signal = df['MACD_Signal'].iloc[-1]
            
            if not pd.isna(macd) and not pd.isna(macd_signal):
                if macd > macd_signal:
                    signals.append("📊 MACD bullish - momentum building")
                else:
                    signals.append("📊 MACD bearish - momentum weakening")
        
        # Volume Analysis
        if 'Volume_Ratio' in df.columns:
            vol_ratio = df['Volume_Ratio'].iloc[-1]
            if vol_ratio > 1.5:
                signals.append("📊 High volume - strong conviction")
            elif vol_ratio < 0.5:
                signals.append("📊 Low volume - weak conviction")
        
        # Price trend analysis
        if len(df) >= 5:
            recent_prices = df['Close'].tail(5)
            if recent_prices.iloc[-1] > recent_prices.iloc[0]:
                signals.append("📈 Recent 5-day uptrend")
            else:
                signals.append("📉 Recent 5-day downtrend")
        
        if not signals:
            signals.append("🤔 No clear signals - consider longer timeframe")
            
    except Exception as e:
        signals.append(f"❌ Analysis error: {str(e)}")
    
    return signals

# Sidebar navigation
st.sidebar.title("🚀 Advanced Learning Hub")
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
    st.markdown('<h1 class="main-header">🚀 Advanced Stock Trading Education Hub</h1>', unsafe_allow_html=True)
    
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
        if st.button("Analyze", type="primary"):
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
    
    # Show sample stocks if no data loaded
    if st.session_state.current_stock is None:
        st.markdown("""
        <div class="info-box">
            <h4>💡 Try these popular stocks:</h4>
            <p><strong>AAPL</strong> - Apple Inc.</p>
            <p><strong>MSFT</strong> - Microsoft Corporation</p>
            <p><strong>GOOGL</strong> - Alphabet Inc.</p>
            <p><strong>TSLA</strong> - Tesla Inc.</p>
            <p><strong>AMZN</strong> - Amazon.com Inc.</p>
        </div>
        """, unsafe_allow_html=True)

# Real-Time Analysis
elif page == "📊 Real-Time Analysis":
    st.markdown('<h1 class="section-header">📊 Real-Time Market Analysis</h1>', unsafe_allow_html=True)
    
    if st.session_state.current_stock:
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
                market_cap = info['marketCap'] / 1e9
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
        <div class="ai-box">
            <h4>🎯 Trading Signals & Insights</h4>
        </div>
        """, unsafe_allow_html=True)
        
        for signal in signals:
            st.markdown(f"• {signal}")
    
    else:
        st.info("Please load a stock from the Dashboard first!")

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

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>📚 Educational content only. Always do your own research and consider consulting with financial advisors.</p>
    <p>Built with ❤️ using Streamlit | Real-time data from Yahoo Finance | AI-powered analysis</p>
</div>
""", unsafe_allow_html=True) 