import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Risk Shield Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #e2e8f0; }
    .stApp { background-color: #0f172a; }
    .metric-card {
        background-color: #1e2937;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #3b82f6;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .success-box { background-color: #14532d; border-left: 5px solid #22c55e; }
    .warning-box { background-color: #78350f; border-left: 5px solid #f59e0b; }
    .danger-box { background-color: #7f1d1d; border-left: 5px solid #ef4444; }
    h1 { color: #60a5fa; }
    .stDataFrame { background-color: #1e2937; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ Risk Shield Pro")
st.markdown("**Professional Statistical Pattern Analyzer** — Discipline meets Probability")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# ==================== SIDEBAR ====================
st.sidebar.header("💰 Capital Controls")
target_profit = st.sidebar.number_input("Target Profit (Ksh)", value=2500, step=500, min_value=500)
stop_loss = st.sidebar.number_input("Stop Loss Limit (Ksh)", value=1200, step=200, min_value=200)
current_pnl = st.sidebar.number_input("Current Session P&L (Ksh)", value=0, step=100)

if current_pnl >= target_profit:
    st.sidebar.success("🎉 TARGET ACHIEVED! Secure Profits.")
elif current_pnl <= -stop_loss:
    st.sidebar.error("🚨 STOP LOSS BREACHED - SESSION TERMINATED")

# ==================== TABS ====================
tab1, tab2, tab3 = st.tabs(["📥 Live Logging", "📊 Analytics", "📜 History"])

with tab1:
    st.subheader("Log New Multiplier")
    with st.form("log_form", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            multiplier = st.number_input("Bust Multiplier", min_value=1.0, value=1.0, step=0.01, format="%.2f")
        with col2:
            submitted = st.form_submit_button("Log Entry", type="primary")
        
        if submitted:
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.history.insert(0, {"time": timestamp, "multiplier": multiplier})
            st.success(f"Logged: {multiplier}x at {timestamp}")

with tab2:
    st.subheader("Analytics Dashboard")
    
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        df['multiplier'] = df['multiplier'].astype(float)
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rounds", len(df))
        with col2:
            red_pct = (df['multiplier'] < 2.0).mean() * 100
            st.metric("Red (<2.0x)", f"{red_pct:.1f}%")
        with col3:
            avg_mult = df['multiplier'].mean()
            st.metric("Average Multiplier", f"{avg_mult:.2f}x")
        with col4:
            max_mult = df['multiplier'].max()
            st.metric("Highest", f"{max_mult:.2f}x")
        
        # Trend Chart
        st.plotly_chart(go.Figure(
            data=go.Scatter(
                x=list(range(len(df))),
                y=df['multiplier'],
                mode='lines+markers',
                name='Multiplier',
                line=dict(color='#60a5fa')
            ),
            layout=go.Layout(
                title="Multiplier Trend",
                xaxis_title="Round (Newest → Oldest)",
                yaxis_title="Multiplier",
                template="plotly_dark",
                height=400,
                shapes=[dict(type="line", y0=2, y1=2, x0=0, x1=len(df), line=dict(color="red", dash="dash"))]
            )
        ), use_container_width=True)
        
        # AI Recommendation
        latest = df.iloc[0]['multiplier']
        streak = 1
        for i in range(1, len(df)):
            if (df.iloc[i]['multiplier'] < 2.0) == (latest < 2.0):
                streak += 1
            else:
                break
        
        st.subheader("🤖 AI Risk Recommendation")
        if latest >= 12.0:
            st.error("🚨 POST-SPIKE RECOVERY PHASE — Sit out next 2-3 rounds")
        elif latest < 2.0 and streak >= 4:
            st.success("🟢 STREAK BREAK LIKELY — Consider tight cashout (1.35x - 1.55x)")
        elif latest >= 2.0 and streak >= 4:
            st.warning("⚠️ GREEN STREAK EXTENDED — High risk of correction")
        else:
            st.info("⚖️ Normal Variance — Play conservatively")
    else:
        st.info("No data yet. Log some multipliers in the Live Logging tab.")

with tab3:
    st.subheader("Session History")
    if st.session_state.history:
        df_display = pd.DataFrame(st.session_state.history)
        st.dataframe(df_display, use_container_width=True)
        
        csv = df_display.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, "risk_shield_history.csv", "text/csv")
    else:
        st.info("History is empty")

# Reset Button
if st.button("🗑️ Clear All Data", type="secondary"):
    st.session_state.history = []
    st.rerun()

st.caption("Risk Shield Pro • Built for disciplined decision making")
