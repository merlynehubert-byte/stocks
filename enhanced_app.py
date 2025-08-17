import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Advanced Stock Trading Education Hub",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling and collapsible sections
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 2rem;
        color: #2e8b57;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .subsection-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .example-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
    .collapsible {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        padding: 0.5rem;
    }
    .collapsible-header {
        cursor: pointer;
        font-weight: bold;
        color: #495057;
    }
    .collapsible-content {
        display: none;
        padding: 1rem;
        border-top: 1px solid #dee2e6;
        margin-top: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem;
        text-align: center;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("📚 Learning Modules")
page = st.sidebar.selectbox(
    "Choose a topic:",
    [
        "🏠 Home & Overview",
        "📊 Stock Basics",
        "🎯 Options Trading",
        "📈 Technical Analysis",
        "💰 Trading Strategies",
        "⏰ Timing & Psychology",
        "📋 Interactive Tools",
        "🔍 Real Examples"
    ]
)

# Real-world examples data
real_examples = {
    "NVDA": {
        "name": "NVIDIA Corporation",
        "current_price": 180.45,
        "change": -1.57,
        "change_pct": -0.86,
        "pe_ratio": 58.21,
        "market_cap": "4.40T",
        "description": "AI chip leader with explosive growth",
        "strategy": "Growth investing",
        "key_metrics": {
            "Revenue Growth": "148.51B",
            "Profit Margin": "51.69%",
            "ROE": "115.46%"
        }
    },
    "TSLA": {
        "name": "Tesla, Inc.",
        "current_price": 330.56,
        "change": -5.02,
        "change_pct": -1.50,
        "pe_ratio": 195.60,
        "market_cap": "1.07T",
        "description": "Electric vehicle and clean energy company",
        "strategy": "Growth investing",
        "key_metrics": {
            "Revenue": "92.72B",
            "Profit Margin": "6.34%",
            "ROE": "8.18%"
        }
    },
    "LEN": {
        "name": "Lennar Corporation",
        "current_price": 130.00,
        "change": 0.00,
        "change_pct": 0.00,
        "pe_ratio": 7.6,
        "market_cap": "36.5B",
        "description": "Home construction company",
        "strategy": "Value investing",
        "key_metrics": {
            "Forward P/E": "7.6",
            "Dividend Yield": "1.2%",
            "Debt/Equity": "0.3"
        }
    },
    "MU": {
        "name": "Micron Technology",
        "current_price": 120.87,
        "change": -4.42,
        "change_pct": -3.53,
        "pe_ratio": 12.4,
        "market_cap": "135.3B",
        "description": "Memory chip manufacturer",
        "strategy": "Value + Growth",
        "key_metrics": {
            "Revenue Growth": "93% YoY",
            "Forward P/E": "12.4",
            "AI Memory Leader": "Yes"
        }
    }
}

# Home page
if page == "🏠 Home & Overview":
    st.markdown('<h1 class="main-header">📈 Advanced Stock Trading Education Hub</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h3>🎯 Your Comprehensive Trading Education Journey</h3>
        <p>This enhanced learning platform combines theoretical knowledge with real-world examples, 
        current market data, and interactive tools to accelerate your trading education.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Current market overview
    st.markdown('<h2 class="subsection-header">📊 Current Market Overview</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">$180.45</div>
            <div class="metric-label">NVIDIA (NVDA)</div>
            <div class="metric-label">-0.86%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">$330.56</div>
            <div class="metric-label">Tesla (TSLA)</div>
            <div class="metric-label">-1.50%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">$130.00</div>
            <div class="metric-label">Lennar (LEN)</div>
            <div class="metric-label">0.00%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">$120.87</div>
            <div class="metric-label">Micron (MU)</div>
            <div class="metric-label">-3.53%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Learning path
    st.markdown('<h2 class="subsection-header">📚 Recommended Learning Path</h2>', unsafe_allow_html=True)
    
    learning_steps = [
        {"step": "1", "title": "Stock Basics", "description": "Understand fundamental concepts", "time": "30 min"},
        {"step": "2", "title": "Options Trading", "description": "Learn calls, puts, and strategies", "time": "45 min"},
        {"step": "3", "title": "Technical Analysis", "description": "Master charts and indicators", "time": "40 min"},
        {"step": "4", "title": "Trading Strategies", "description": "Apply different approaches", "time": "35 min"},
        {"step": "5", "title": "Real Examples", "description": "Study current market cases", "time": "30 min"},
        {"step": "6", "title": "Interactive Tools", "description": "Practice with calculators", "time": "20 min"}
    ]
    
    for step in learning_steps:
        with st.expander(f"Step {step['step']}: {step['title']} ({step['time']})"):
            st.markdown(f"**{step['description']}**")
            st.markdown(f"Estimated time: {step['time']}")

# Stock Basics with collapsible sections
elif page == "📊 Stock Basics":
    st.markdown('<h1 class="section-header">📊 Stock Market Fundamentals</h1>', unsafe_allow_html=True)
    
    # What are Stocks
    with st.expander("📋 What are Stocks?", expanded=True):
        st.markdown("""
        **Stocks represent ownership in a company.** When you buy a stock, you're purchasing a small piece of that company, 
        called a "share" or "equity."
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### ✅ Benefits of Stock Ownership
            - **Dividends**: Regular payments from company profits
            - **Capital Gains**: Profit when selling at higher price
            - **Voting Rights**: Say in company decisions
            - **Limited Liability**: You can't lose more than you invested
            """)
        
        with col2:
            st.markdown("""
            ### ⚠️ Risks of Stock Ownership
            - **Market Risk**: Stock prices can fall
            - **Company Risk**: Business may fail
            - **Liquidity Risk**: May not sell when needed
            - **Inflation Risk**: Money loses value over time
            """)
    
    # Market Types
    with st.expander("🐂🐻 Bull vs Bear Markets"):
        st.markdown("""
        ### 🐂 Bull Market vs 🐻 Bear Market
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🐂 Bull Market**
            - Rising stock prices
            - Optimistic investor sentiment
            - Economic growth
            - Good time to buy and hold
            """)
        
        with col2:
            st.markdown("""
            **🐻 Bear Market**
            - Falling stock prices
            - Pessimistic sentiment
            - Economic downturn
            - Opportunities for value buying
            """)
    
    # Order Types
    with st.expander("📝 Order Types"):
        order_types = {
            "Market Order": "Buy/sell immediately at current market price",
            "Limit Order": "Buy/sell at a specific price or better",
            "Stop Order": "Sell when price falls to a certain level",
            "Stop-Limit Order": "Combines stop and limit order features"
        }
        
        for order_type, description in order_types.items():
            st.markdown(f"**{order_type}**: {description}")
    
    # Risk Management
    with st.expander("🛡️ Risk Management"):
        st.markdown("""
        <div class="warning-box">
            <h4>Golden Rule: Never invest more than you can afford to lose!</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### Key Risk Management Principles:
        1. **Diversification**: Don't put all eggs in one basket
        2. **Position Sizing**: Limit each investment to 1-5% of portfolio
        3. **Stop Losses**: Set automatic sell orders to limit losses
        4. **Research**: Always understand what you're buying
        5. **Long-term Perspective**: Don't panic over short-term fluctuations
        """)

# Options Trading with real examples
elif page == "🎯 Options Trading":
    st.markdown('<h1 class="section-header">🎯 Options Trading Masterclass</h1>', unsafe_allow_html=True)
    
    # Options Basics
    with st.expander("📋 What are Options?", expanded=True):
        st.markdown("""
        **Options are contracts that give you the right (but not obligation) to buy or sell a stock at a specific price by a certain date.**
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### 📋 Key Terms
            - **Strike Price**: Price at which you can buy/sell
            - **Expiration Date**: When the option expires
            - **Premium**: Cost of the option contract
            - **In-the-Money**: Option has intrinsic value
            - **Out-of-the-Money**: Option has no intrinsic value
            """)
        
        with col2:
            st.markdown("""
            ### 💰 Why Trade Options?
            - **Leverage**: Control more stock with less money
            - **Hedging**: Protect against losses
            - **Income**: Generate cash flow
            - **Flexibility**: Multiple strategies available
            """)
    
    # Call Options
    with st.expander("📞 Call Options Deep Dive"):
        st.markdown('<h3 class="subsection-header">📞 Long Call (Buying Calls)</h3>', unsafe_allow_html=True)
        st.markdown("**When to use**: When you expect stock price to rise significantly")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **✅ Advantages:**
            - Unlimited profit potential
            - Limited risk (only premium paid)
            - Leverage (control 100 shares with less capital)
            """)
        
        with col2:
            st.markdown("""
            **❌ Disadvantages:**
            - Time decay works against you
            - Need significant price movement to profit
            - Can lose entire premium if stock doesn't move
            """)
        
        # Real example
        st.markdown("""
        <div class="example-box">
            <h4>🎯 Real Example: NVIDIA (NVDA) Call Option</h4>
            <p><strong>Scenario:</strong> NVDA is at $180.45, you expect it to rise to $200</p>
            <p><strong>Trade:</strong> Buy NVDA $185 Call expiring in 30 days for $3.50</p>
            <p><strong>Cost:</strong> $350 (100 shares × $3.50)</p>
            <p><strong>Break-even:</strong> $188.50 ($185 + $3.50)</p>
            <p><strong>Profit at $200:</strong> $1,150 (($200 - $188.50) × 100)</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Put Options
    with st.expander("📞 Put Options Deep Dive"):
        st.markdown('<h3 class="subsection-header">📞 Long Put (Buying Puts)</h3>', unsafe_allow_html=True)
        st.markdown("**When to use**: When you expect stock price to fall significantly")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **✅ Advantages:**
            - Profit from falling stock prices
            - Limited risk (only premium paid)
            - Can be used for hedging
            """)
        
        with col2:
            st.markdown("""
            **❌ Disadvantages:**
            - Time decay works against you
            - Need significant price drop to profit
            - Can lose entire premium
            """)
        
        # Real example
        st.markdown("""
        <div class="example-box">
            <h4>🎯 Real Example: Tesla (TSLA) Put Option</h4>
            <p><strong>Scenario:</strong> TSLA is at $330.56, you expect it to fall to $300</p>
            <p><strong>Trade:</strong> Buy TSLA $325 Put expiring in 30 days for $8.00</p>
            <p><strong>Cost:</strong> $800 (100 shares × $8.00)</p>
            <p><strong>Break-even:</strong> $317 ($325 - $8.00)</p>
            <p><strong>Profit at $300:</strong> $1,700 (($325 - $300) × 100 - $800)</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Options Strategies
    with st.expander("🎯 Popular Options Strategies"):
        strategies = {
            "Covered Call": "Sell calls against stock you own - generates income",
            "Cash Secured Put": "Sell puts with cash to back them - income + potential stock acquisition",
            "Iron Condor": "Sell both calls and puts - profits from sideways movement",
            "Butterfly Spread": "Limited risk, limited reward - profits from specific price target",
            "Straddle": "Buy both call and put - profits from large price movement in either direction"
        }
        
        for strategy, description in strategies.items():
            st.markdown(f"**{strategy}**: {description}")

# Technical Analysis with charts
elif page == "📈 Technical Analysis":
    st.markdown('<h1 class="section-header">📈 Technical Analysis & Indicators</h1>', unsafe_allow_html=True)
    
    # Moving Averages
    with st.expander("📊 Moving Averages", expanded=True):
        st.markdown('<h3 class="subsection-header">📊 Moving Averages</h3>', unsafe_allow_html=True)
        
        # Create sample moving average chart
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        prices = 100 + np.cumsum(np.random.randn(100) * 0.5)
        df = pd.DataFrame({'Date': dates, 'Price': prices})
        df['SMA_20'] = df['Price'].rolling(window=20).mean()
        df['SMA_50'] = df['Price'].rolling(window=50).mean()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Price'], name='Stock Price', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_20'], name='20-day SMA', line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_50'], name='50-day SMA', line=dict(color='red')))
        
        fig.update_layout(
            title='Moving Averages Example',
            xaxis_title='Date',
            yaxis_title='Price',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        ### 📊 Types of Moving Averages
        - **Simple Moving Average (SMA)**: Average of prices over period
        - **Exponential Moving Average (EMA)**: Gives more weight to recent prices
        - **Weighted Moving Average (WMA)**: Custom weighting system
        
        ### 🎯 Trading Signals
        - **Golden Cross**: Short-term MA crosses above long-term MA (bullish)
        - **Death Cross**: Short-term MA crosses below long-term MA (bearish)
        - **Support/Resistance**: Price bounces off moving averages
        """)
    
    # Momentum Indicators
    with st.expander("📊 Momentum Indicators"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 📊 RSI (Relative Strength Index)
            - Measures speed and magnitude of price changes
            - Range: 0-100
            - **Overbought**: Above 70 (potential sell signal)
            - **Oversold**: Below 30 (potential buy signal)
            """)
        
        with col2:
            st.markdown("""
            ### 📊 MACD (Moving Average Convergence Divergence)
            - Shows relationship between two moving averages
            - **Bullish**: MACD line crosses above signal line
            - **Bearish**: MACD line crosses below signal line
            - **Divergence**: Price and MACD moving in opposite directions
            """)
    
    # Chart Patterns
    with st.expander("📈 Chart Patterns"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 📈 Bullish Patterns
            - **Double Bottom**: W-shaped pattern indicating reversal
            - **Cup and Handle**: U-shaped pattern with small pullback
            - **Ascending Triangle**: Rising support with flat resistance
            - **Flag/Pennant**: Brief consolidation after strong move
            """)
        
        with col2:
            st.markdown("""
            ### 📉 Bearish Patterns
            - **Double Top**: M-shaped pattern indicating reversal
            - **Head and Shoulders**: Three-peak pattern with middle peak highest
            - **Descending Triangle**: Falling resistance with flat support
            - **Wedge**: Converging trend lines
            """)

# Trading Strategies with real examples
elif page == "💰 Trading Strategies":
    st.markdown('<h1 class="section-header">💰 Trading Strategies & When to Use Them</h1>', unsafe_allow_html=True)
    
    # Value Investing
    with st.expander("💰 Value Investing", expanded=True):
        st.markdown('<h3 class="subsection-header">💰 Value Investing</h3>', unsafe_allow_html=True)
        st.markdown("**Value investing focuses on finding stocks that are trading below their intrinsic value.**")
        
        st.markdown("""
        ### 🎯 Key Principles
        - **Margin of Safety**: Buy at significant discount to intrinsic value
        - **Long-term Perspective**: Hold for years, not days
        - **Fundamental Analysis**: Focus on company financials
        - **Contrarian Approach**: Buy when others are selling
        """)
        
        # Real example
        st.markdown("""
        <div class="example-box">
            <h4>🎯 Real Example: Lennar Corporation (LEN)</h4>
            <p><strong>Current Price:</strong> $130.00</p>
            <p><strong>Forward P/E:</strong> 7.6 (vs market average ~20)</p>
            <p><strong>Strategy:</strong> Value investing - trading at significant discount</p>
            <p><strong>Catalyst:</strong> Strong housing demand, cost controls, positive outlook</p>
            <p><strong>Risk/Reward:</strong> Limited downside, 25%+ upside potential</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Growth Investing
    with st.expander("📈 Growth Investing"):
        st.markdown('<h3 class="subsection-header">📈 Growth Investing</h3>', unsafe_allow_html=True)
        st.markdown("**Growth investing focuses on companies with above-average growth potential.**")
        
        st.markdown("""
        ### 🎯 Key Principles
        - **Revenue Growth**: Look for companies growing sales rapidly
        - **Market Expansion**: Companies entering new markets
        - **Innovation**: Companies with competitive advantages
        - **High P/E Acceptable**: Pay premium for growth potential
        """)
        
        # Real example
        st.markdown("""
        <div class="example-box">
            <h4>🎯 Real Example: NVIDIA Corporation (NVDA)</h4>
            <p><strong>Current Price:</strong> $180.45</p>
            <p><strong>P/E Ratio:</strong> 58.21 (high but justified by growth)</p>
            <p><strong>Revenue Growth:</strong> $148.51B (explosive AI growth)</p>
            <p><strong>Strategy:</strong> Growth investing - AI leadership position</p>
            <p><strong>Catalyst:</strong> AI chip demand, data center expansion</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Day Trading
    with st.expander("⚡ Day Trading"):
        st.markdown('<h3 class="subsection-header">⚡ Day Trading</h3>', unsafe_allow_html=True)
        st.markdown("**Day trading involves buying and selling stocks within the same trading day.**")
        
        st.markdown("""
        <div class="warning-box">
            <h4>⚠️ High Risk Warning</h4>
            <p>Day trading is extremely risky and requires significant capital, time, and emotional control. 
            Most day traders lose money. Only attempt with proper education and risk management.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### 🎯 Key Principles
        - **Technical Analysis**: Focus on charts and patterns
        - **Volume Analysis**: High volume confirms moves
        - **Risk Management**: Strict stop losses (1-2% per trade)
        - **Emotional Control**: Don't let fear/greed drive decisions
        """)

# Real Examples page
elif page == "🔍 Real Examples":
    st.markdown('<h1 class="section-header">🔍 Real-World Trading Examples</h1>', unsafe_allow_html=True)
    
    # Select stock to analyze
    selected_stock = st.selectbox("Choose a stock to analyze:", list(real_examples.keys()))
    
    if selected_stock:
        stock_data = real_examples[selected_stock]
        
        st.markdown(f"""
        <div class="info-box">
            <h3>📊 {stock_data['name']} ({selected_stock}) Analysis</h3>
            <p><strong>Current Price:</strong> ${stock_data['current_price']} ({stock_data['change']:+.2f}, {stock_data['change_pct']:+.2f}%)</p>
            <p><strong>Market Cap:</strong> ${stock_data['market_cap']}</p>
            <p><strong>P/E Ratio:</strong> {stock_data['pe_ratio']}</p>
            <p><strong>Strategy:</strong> {stock_data['strategy']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Key metrics
        st.markdown('<h3 class="subsection-header">📈 Key Metrics</h3>', unsafe_allow_html=True)
        
        cols = st.columns(len(stock_data['key_metrics']))
        for i, (metric, value) in enumerate(stock_data['key_metrics'].items()):
            with cols[i]:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{value}</div>
                    <div class="metric-label">{metric}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Trading scenarios
        st.markdown('<h3 class="subsection-header">🎯 Trading Scenarios</h3>', unsafe_allow_html=True)
        
        if selected_stock == "NVDA":
            st.markdown("""
            <div class="example-box">
                <h4>📈 Growth Investing Scenario</h4>
                <p><strong>Entry:</strong> Buy NVDA at $180.45</p>
                <p><strong>Target:</strong> $220 (22% upside)</p>
                <p><strong>Stop Loss:</strong> $160 (11% downside)</p>
                <p><strong>Rationale:</strong> AI leadership, strong fundamentals, growth trajectory</p>
            </div>
            """, unsafe_allow_html=True)
        
        elif selected_stock == "LEN":
            st.markdown("""
            <div class="example-box">
                <h4>💰 Value Investing Scenario</h4>
                <p><strong>Entry:</strong> Buy LEN at $130.00</p>
                <p><strong>Target:</strong> $160 (23% upside)</p>
                <p><strong>Stop Loss:</strong> $115 (12% downside)</p>
                <p><strong>Rationale:</strong> Undervalued P/E, housing market recovery, strong balance sheet</p>
            </div>
            """, unsafe_allow_html=True)
        
        elif selected_stock == "TSLA":
            st.markdown("""
            <div class="example-box">
                <h4>📈 Growth Investing Scenario</h4>
                <p><strong>Entry:</strong> Buy TSLA at $330.56</p>
                <p><strong>Target:</strong> $400 (21% upside)</p>
                <p><strong>Stop Loss:</strong> $280 (15% downside)</p>
                <p><strong>Rationale:</strong> EV market leadership, innovation, global expansion</p>
            </div>
            """, unsafe_allow_html=True)

# Interactive Tools
elif page == "📋 Interactive Tools":
    st.markdown('<h1 class="section-header">📋 Interactive Learning Tools</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Options Calculator", "Risk Calculator", "Quiz"])
    
    with tab1:
        st.markdown('<h2 class="subsection-header">Options Profit Calculator</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            option_type = st.selectbox("Option Type", ["Call", "Put"])
            action = st.selectbox("Action", ["Buy", "Sell"])
            strike_price = st.number_input("Strike Price ($)", min_value=1.0, value=50.0, step=1.0)
            premium = st.number_input("Premium ($)", min_value=0.01, value=2.0, step=0.01)
        
        with col2:
            current_price = st.number_input("Current Stock Price ($)", min_value=1.0, value=50.0, step=1.0)
            shares_per_contract = st.number_input("Shares per Contract", min_value=1, value=100, step=1)
        
        # Calculate profit/loss
        if option_type == "Call":
            if action == "Buy":
                if current_price > strike_price:
                    intrinsic_value = current_price - strike_price
                    profit = (intrinsic_value - premium) * shares_per_contract
                else:
                    profit = -premium * shares_per_contract
            else:  # Sell
                if current_price > strike_price:
                    intrinsic_value = current_price - strike_price
                    profit = (premium - intrinsic_value) * shares_per_contract
                else:
                    profit = premium * shares_per_contract
        else:  # Put
            if action == "Buy":
                if current_price < strike_price:
                    intrinsic_value = strike_price - current_price
                    profit = (intrinsic_value - premium) * shares_per_contract
                else:
                    profit = -premium * shares_per_contract
            else:  # Sell
                if current_price < strike_price:
                    intrinsic_value = strike_price - current_price
                    profit = (premium - intrinsic_value) * shares_per_contract
                else:
                    profit = premium * shares_per_contract
        
        st.markdown(f"""
        ### 📊 Results
        **Option**: {action} {option_type}  
        **Strike**: ${strike_price}  
        **Premium**: ${premium}  
        **Current Price**: ${current_price}  
        **Profit/Loss**: ${profit:.2f}
        """)
        
        if profit > 0:
            st.success(f"✅ This trade would be profitable: ${profit:.2f}")
        else:
            st.error(f"❌ This trade would lose money: ${profit:.2f}")
    
    with tab2:
        st.markdown('<h2 class="subsection-header">Risk Management Calculator</h2>', unsafe_allow_html=True)
        
        portfolio_value = st.number_input("Portfolio Value ($)", min_value=1000, value=10000, step=1000)
        risk_per_trade = st.slider("Risk per Trade (%)", min_value=0.5, max_value=5.0, value=1.0, step=0.1)
        stop_loss_pct = st.slider("Stop Loss (%)", min_value=1.0, max_value=20.0, value=5.0, step=0.5)
        
        risk_amount = portfolio_value * (risk_per_trade / 100)
        position_size = risk_amount / (stop_loss_pct / 100)
        
        st.markdown(f"""
        ### 📊 Risk Calculation Results
        **Portfolio Value**: ${portfolio_value:,}  
        **Risk per Trade**: ${risk_amount:.2f} ({risk_per_trade}%)  
        **Stop Loss**: {stop_loss_pct}%  
        **Maximum Position Size**: ${position_size:.2f}
        """)
        
        st.markdown("""
        ### 💡 Interpretation
        This means you should never risk more than ${risk_amount:.2f} on any single trade, 
        and with a {stop_loss_pct}% stop loss, your maximum position size should be ${position_size:.2f}.
        """)
    
    with tab3:
        st.markdown('<h2 class="subsection-header">Trading Knowledge Quiz</h2>', unsafe_allow_html=True)
        
        questions = [
            {
                "question": "What is a 'long call' option?",
                "options": [
                    "Selling a call option",
                    "Buying a call option",
                    "Both buying and selling calls",
                    "A type of put option"
                ],
                "correct": 1
            },
            {
                "question": "What does RSI stand for?",
                "options": [
                    "Relative Strength Index",
                    "Random Stock Indicator",
                    "Rate of Stock Increase",
                    "Real Stock Investment"
                ],
                "correct": 0
            },
            {
                "question": "What is the 'Golden Cross'?",
                "options": [
                    "When gold prices rise",
                    "When short-term MA crosses above long-term MA",
                    "When stock hits all-time high",
                    "A type of options strategy"
                ],
                "correct": 1
            },
            {
                "question": "What is the maximum loss when buying a call option?",
                "options": [
                    "Unlimited",
                    "The premium paid",
                    "The strike price",
                    "The current stock price"
                ],
                "correct": 1
            },
            {
                "question": "What is a 'stop loss'?",
                "options": [
                    "A guaranteed profit order",
                    "An order to sell at a specific price to limit losses",
                    "A type of dividend",
                    "A market timing indicator"
                ],
                "correct": 1
            }
        ]
        
        if 'quiz_answers' not in st.session_state:
            st.session_state.quiz_answers = {}
        
        score = 0
        for i, q in enumerate(questions):
            st.markdown(f"**Question {i+1}**: {q['question']}")
            answer = st.radio(f"Select your answer:", q['options'], key=f"q{i}")
            st.session_state.quiz_answers[i] = answer
            
            if st.session_state.quiz_answers[i] == q['options'][q['correct']]:
                score += 1
        
        if st.button("Submit Quiz"):
            percentage = (score / len(questions)) * 100
            st.markdown(f"### 📊 Quiz Results")
            st.markdown(f"**Score**: {score}/{len(questions)} ({percentage:.1f}%)")
            
            if percentage >= 80:
                st.success("🎉 Excellent! You have a strong understanding of trading concepts!")
            elif percentage >= 60:
                st.warning("📚 Good! Keep studying to improve your knowledge.")
            else:
                st.error("📖 Keep learning! Review the material and try again.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>📚 Educational content only. Always do your own research and consider consulting with financial advisors.</p>
    <p>Built with ❤️ using Streamlit | Data from Yahoo Finance</p>
</div>
""", unsafe_allow_html=True) 