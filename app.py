import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Stock Trading Education Hub",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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
        "📈 Technical Indicators",
        "💰 Trading Strategies",
        "⏰ Timing & Psychology",
        "📋 Interactive Tools"
    ]
)

# Home page
if page == "🏠 Home & Overview":
    st.markdown('<h1 class="main-header">📈 Stock Trading Education Hub</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h3>Welcome to Your Trading Education Journey!</h3>
        <p>This comprehensive learning platform will guide you through the fundamentals of stock trading and investing. 
        Whether you're a complete beginner or looking to refine your skills, you'll find valuable insights here.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🎯 What You'll Learn
        - Stock market fundamentals
        - Options trading strategies
        - Technical analysis
        - Risk management
        - Trading psychology
        """)
    
    with col2:
        st.markdown("""
        ### 📚 Learning Path
        1. **Stock Basics** - Foundation concepts
        2. **Options Trading** - Calls, puts, strategies
        3. **Technical Indicators** - Charts and analysis
        4. **Trading Strategies** - When to buy/sell
        5. **Timing & Psychology** - Market timing
        """)
    
    with col3:
        st.markdown("""
        ### ⚠️ Important Disclaimer
        This is for educational purposes only. 
        Always do your own research and consider consulting with financial advisors before making investment decisions.
        """)

# Stock Basics
elif page == "📊 Stock Basics":
    st.markdown('<h1 class="section-header">📊 Stock Market Fundamentals</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["What are Stocks", "Market Types", "Order Types", "Risk Management"])
    
    with tab1:
        st.markdown('<h2 class="subsection-header">What are Stocks?</h2>', unsafe_allow_html=True)
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
    
    with tab2:
        st.markdown('<h2 class="subsection-header">Market Types</h2>', unsafe_allow_html=True)
        
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
    
    with tab3:
        st.markdown('<h2 class="subsection-header">Order Types</h2>', unsafe_allow_html=True)
        
        order_types = {
            "Market Order": "Buy/sell immediately at current market price",
            "Limit Order": "Buy/sell at a specific price or better",
            "Stop Order": "Sell when price falls to a certain level",
            "Stop-Limit Order": "Combines stop and limit order features"
        }
        
        for order_type, description in order_types.items():
            st.markdown(f"**{order_type}**: {description}")
    
    with tab4:
        st.markdown('<h2 class="subsection-header">Risk Management</h2>', unsafe_allow_html=True)
        
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

# Options Trading
elif page == "🎯 Options Trading":
    st.markdown('<h1 class="section-header">🎯 Options Trading Masterclass</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Options Basics", "Call Options", "Put Options", "Strategies"])
    
    with tab1:
        st.markdown('<h2 class="subsection-header">What are Options?</h2>', unsafe_allow_html=True)
        
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
    
    with tab2:
        st.markdown('<h2 class="subsection-header">Call Options Deep Dive</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        ### 📞 Long Call (Buying Calls)
        **When to use**: When you expect stock price to rise significantly
        """)
        
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
        
        st.markdown("""
        ### 📞 Short Call (Selling Calls)
        **When to use**: When you expect stock to stay flat or decline slightly
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **✅ Advantages:**
            - Collect premium income
            - Time decay works in your favor
            - Can profit in sideways markets
            """)
        
        with col2:
            st.markdown("""
            **❌ Disadvantages:**
            - Unlimited loss potential
            - Requires margin account
            - Can be assigned early
            """)
    
    with tab3:
        st.markdown('<h2 class="subsection-header">Put Options Deep Dive</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        ### 📞 Long Put (Buying Puts)
        **When to use**: When you expect stock price to fall significantly
        """)
        
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
        
        st.markdown("""
        ### 📞 Short Put (Selling Puts)
        **When to use**: When you expect stock to stay flat or rise slightly
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **✅ Advantages:**
            - Collect premium income
            - Time decay works in your favor
            - Can acquire stock at lower price if assigned
            """)
        
        with col2:
            st.markdown("""
            **❌ Disadvantages:**
            - Large loss potential if stock crashes
            - Requires margin account
            - Can be assigned early
            """)
    
    with tab4:
        st.markdown('<h2 class="subsection-header">Popular Options Strategies</h2>', unsafe_allow_html=True)
        
        strategies = {
            "Covered Call": "Sell calls against stock you own - generates income",
            "Cash Secured Put": "Sell puts with cash to back them - income + potential stock acquisition",
            "Iron Condor": "Sell both calls and puts - profits from sideways movement",
            "Butterfly Spread": "Limited risk, limited reward - profits from specific price target",
            "Straddle": "Buy both call and put - profits from large price movement in either direction"
        }
        
        for strategy, description in strategies.items():
            st.markdown(f"**{strategy}**: {description}")

# Technical Indicators
elif page == "📈 Technical Indicators":
    st.markdown('<h1 class="section-header">📈 Technical Analysis & Indicators</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Moving Averages", "Momentum Indicators", "Volume Indicators", "Chart Patterns"])
    
    with tab1:
        st.markdown('<h2 class="subsection-header">Moving Averages</h2>', unsafe_allow_html=True)
        
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
    
    with tab2:
        st.markdown('<h2 class="subsection-header">Momentum Indicators</h2>', unsafe_allow_html=True)
        
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
        
        st.markdown("""
        ### 📊 Stochastic Oscillator
        - Compares closing price to price range over time
        - **Overbought**: Above 80
        - **Oversold**: Below 20
        - **K% and D% lines**: Fast and slow stochastic lines
        """)
    
    with tab3:
        st.markdown('<h2 class="subsection-header">Volume Indicators</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        ### 📊 Volume Analysis
        Volume is crucial for confirming price movements and identifying potential reversals.
        """)
        
        indicators = {
            "On-Balance Volume (OBV)": "Cumulative volume indicator that adds volume on up days and subtracts on down days",
            "Volume Rate of Change": "Measures the speed of volume changes",
            "Money Flow Index": "Combines price and volume to identify overbought/oversold conditions",
            "Accumulation/Distribution Line": "Shows whether money is flowing into or out of a stock"
        }
        
        for indicator, description in indicators.items():
            st.markdown(f"**{indicator}**: {description}")
    
    with tab4:
        st.markdown('<h2 class="subsection-header">Chart Patterns</h2>', unsafe_allow_html=True)
        
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

# Trading Strategies
elif page == "💰 Trading Strategies":
    st.markdown('<h1 class="section-header">💰 Trading Strategies & When to Use Them</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Value Investing", "Growth Investing", "Day Trading", "Swing Trading"])
    
    with tab1:
        st.markdown('<h2 class="subsection-header">Value Investing</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        **Value investing focuses on finding stocks that are trading below their intrinsic value.**
        """)
        
        st.markdown("""
        ### 🎯 Key Principles
        - **Margin of Safety**: Buy at significant discount to intrinsic value
        - **Long-term Perspective**: Hold for years, not days
        - **Fundamental Analysis**: Focus on company financials
        - **Contrarian Approach**: Buy when others are selling
        """)
        
        st.markdown("""
        ### 📊 Key Metrics to Analyze
        - **P/E Ratio**: Price-to-earnings ratio
        - **P/B Ratio**: Price-to-book ratio
        - **Debt-to-Equity**: Company's financial leverage
        - **ROE**: Return on equity
        - **Free Cash Flow**: Cash available after expenses
        """)
        
        st.markdown("""
        ### ⏰ When to Buy/Sell
        - **Buy**: When stock is undervalued based on fundamentals
        - **Sell**: When stock reaches fair value or fundamentals deteriorate
        - **Hold**: As long as company fundamentals remain strong
        """)
    
    with tab2:
        st.markdown('<h2 class="subsection-header">Growth Investing</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        **Growth investing focuses on companies with above-average growth potential.**
        """)
        
        st.markdown("""
        ### 🎯 Key Principles
        - **Revenue Growth**: Look for companies growing sales rapidly
        - **Market Expansion**: Companies entering new markets
        - **Innovation**: Companies with competitive advantages
        - **High P/E Acceptable**: Pay premium for growth potential
        """)
        
        st.markdown("""
        ### 📊 Key Metrics to Analyze
        - **Revenue Growth Rate**: Year-over-year sales growth
        - **Earnings Growth Rate**: Year-over-year profit growth
        - **Market Share**: Company's position in industry
        - **R&D Spending**: Investment in future growth
        - **Customer Acquisition**: New customer growth rate
        """)
        
        st.markdown("""
        ### ⏰ When to Buy/Sell
        - **Buy**: When growth story is intact and expanding
        - **Sell**: When growth slows or competitive advantages erode
        - **Hold**: During temporary setbacks if long-term story unchanged
        """)
    
    with tab3:
        st.markdown('<h2 class="subsection-header">Day Trading</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        **Day trading involves buying and selling stocks within the same trading day.**
        """)
        
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
        
        st.markdown("""
        ### 📊 Key Indicators for Day Trading
        - **Level 2 Quotes**: Real-time bid/ask data
        - **Volume Profile**: Where most trading occurs
        - **Support/Resistance**: Key price levels
        - **Momentum Indicators**: RSI, MACD, Stochastic
        """)
    
    with tab4:
        st.markdown('<h2 class="subsection-header">Swing Trading</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        **Swing trading holds positions for days to weeks, capturing medium-term moves.**
        """)
        
        st.markdown("""
        ### 🎯 Key Principles
        - **Trend Following**: Trade in direction of larger trend
        - **Pullback Entries**: Buy dips in uptrends, sell rallies in downtrends
        - **Risk/Reward**: Aim for 2:1 or better risk/reward ratio
        - **Position Sizing**: 1-5% of portfolio per trade
        """)
        
        st.markdown("""
        ### 📊 Entry/Exit Strategies
        - **Entry**: Breakout above resistance or bounce off support
        - **Stop Loss**: Below recent swing low (long) or above swing high (short)
        - **Take Profit**: At next resistance level or 2:1 risk/reward
        - **Time Stop**: Exit if trade doesn't work within expected timeframe
        """)

# Timing & Psychology
elif page == "⏰ Timing & Psychology":
    st.markdown('<h1 class="section-header">⏰ Market Timing & Trading Psychology</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Market Cycles", "Psychology", "Risk Management", "Common Mistakes"])
    
    with tab1:
        st.markdown('<h2 class="subsection-header">Market Cycles</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        ### 📈 Understanding Market Cycles
        Markets move in cycles, and understanding these can help with timing.
        """)
        
        cycles = {
            "Accumulation": "Smart money starts buying when others are fearful",
            "Markup": "Price begins to rise, more investors notice",
            "Distribution": "Smart money starts selling to retail investors",
            "Markdown": "Price falls as selling pressure increases"
        }
        
        for phase, description in cycles.items():
            st.markdown(f"**{phase}**: {description}")
        
        st.markdown("""
        ### 🕐 Time-Based Patterns
        - **January Effect**: Small caps often outperform in January
        - **Sell in May**: Historical underperformance May-October
        - **Earnings Season**: Increased volatility around earnings
        - **Fed Meetings**: Market reactions to interest rate decisions
        """)
    
    with tab2:
        st.markdown('<h2 class="subsection-header">Trading Psychology</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        **Psychology is often more important than strategy in trading success.**
        """)
        
        emotions = {
            "Fear": "Causes selling at bottoms, missing opportunities",
            "Greed": "Causes buying at tops, holding too long",
            "Hope": "Prevents cutting losses, leads to bigger losses",
            "Regret": "Causes overtrading to recover losses"
        }
        
        st.markdown("### 😰 Common Emotional Traps")
        for emotion, impact in emotions.items():
            st.markdown(f"**{emotion}**: {impact}")
        
        st.markdown("""
        ### 🧠 Psychological Tools
        - **Trading Journal**: Record all trades and emotions
        - **Meditation**: Reduce stress and improve focus
        - **Breaks**: Step away when emotions are high
        - **Accountability**: Share trades with trusted mentor
        """)
    
    with tab3:
        st.markdown('<h2 class="subsection-header">Risk Management</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="success-box">
            <h4>🎯 Golden Rule: Risk management is more important than finding winning trades!</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### 📊 Position Sizing Rules
        - **1% Rule**: Risk no more than 1% of portfolio per trade
        - **5% Rule**: No single position should exceed 5% of portfolio
        - **20% Rule**: No single sector should exceed 20% of portfolio
        """)
        
        st.markdown("""
        ### 🛡️ Stop Loss Strategies
        - **Fixed Percentage**: 2-3% below entry price
        - **Support Level**: Below recent support level
        - **ATR-Based**: Based on Average True Range
        - **Trailing Stop**: Moves up as price rises
        """)
        
        st.markdown("""
        ### 📈 Take Profit Strategies
        - **Risk/Reward Ratio**: Aim for 2:1 or 3:1
        - **Resistance Levels**: Sell at key resistance
        - **Partial Profits**: Take some profits at targets
        - **Trailing Profits**: Let winners run with trailing stops
        """)
    
    with tab4:
        st.markdown('<h2 class="subsection-header">Common Trading Mistakes</h2>', unsafe_allow_html=True)
        
        mistakes = {
            "Overtrading": "Trading too frequently without proper analysis",
            "No Stop Loss": "Not having exit plan leads to big losses",
            "Revenge Trading": "Trying to recover losses with bigger positions",
            "FOMO": "Fear of missing out leads to poor entries",
            "Averaging Down": "Adding to losing positions without analysis",
            "Ignoring Fundamentals": "Only using technical analysis",
            "Not Diversifying": "Putting all money in one stock/sector",
            "Trading on Margin": "Using borrowed money increases risk"
        }
        
        st.markdown("### ❌ Mistakes to Avoid")
        for mistake, description in mistakes.items():
            st.markdown(f"**{mistake}**: {description}")

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
    <p>Built with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True) 