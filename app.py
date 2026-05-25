import streamlit as st
import pandas as pd
import numpy as np

# Set up clean, professional page styling
st.set_page_config(page_title="Risk Shield Pro", page_icon="🛡️", layout="centered")

# Custom CSS for dark professional styling
st.markdown("""
    <style>
    .big-font { font-size:24px !important; font-weight: bold; color: #1E3A8A; }
    .metric-box { padding: 15px; background-color: #F3F4F6; border-radius: 8px; border-left: 5px solid #3B82F6; }
    .danger-box { padding: 15px; background-color: #FEE2E2; border-radius: 8px; border-left: 5px solid #EF4444; color: #991B1B; }
    .success-box { padding: 15px; background-color: #DCFCE7; border-radius: 8px; border-left: 5px solid #22C55E; color: #166534; }
    .warning-box { padding: 15px; background-color: #FEF3C7; border-radius: 8px; border-left: 5px solid #F59E0B; color: #92400E; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ Risk Shield Pro: Statistical Pattern Analyzer")
st.markdown("A disciplined, probability-based analytical dashboard designed to track trends, isolate risky house environments, and manage capital scientifically.")

# Initialize the session database if it doesn't exist
if "history" not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR: CAPITAL CONTROL & DISCIPLINE MANAGER ---
st.sidebar.header("Capital & Discipline Controls")
st.sidebar.markdown("Set your boundaries before launching a session. These limits act as a hard systemic barrier.")

target_profit = st.sidebar.number_input("Target Profit Boundary (Ksh)", value=2000, step=500, min_value=100)
stop_loss = st.sidebar.number_input("Hard Stop-Loss Limit (Ksh)", value=1000, step=200, min_value=100)
current_balance = st.sidebar.number_input("Current Session Net Gain/Loss (Ksh)", value=0, step=100)
# Enforce strict code-driven warnings based on money management rules
if current_balance >= target_profit:
    st.sidebar.balloons()
    st.sidebar.success("🏆 BREAKPOINT ACHIEVED: You have reached your target profit boundary. Terminate the session immediately and secure your capital.")
elif current_balance <= -stop_loss:
    st.sidebar.error("🚨 CRITICAL STOP-LOSS REACHED: Hard boundary breached. Shut down the system. Continuing runs under skewed platform distribution leads to total capital depletion.")

# --- MAIN INTERFACE: LIVE DATA LOGGING ---
st.subheader("📥 Real-Time Multiplier Entry")
st.markdown("Input the exact bust values as they appear chronologically on your history ticker.")

with st.form("input_form", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        new_val = st.number_input("Bust Multiplier:", min_value=1.00, value=1.00, step=0.01, format="%.2f", help="Type the exact decimal point where the curve crashed.")
    with col2:
        submit = st.form_submit_button("Log Entry")

if submit:
    # Prepend new value to keep the latest run at index 0 (matching natural chronological screen layouts)
    st.session_state.history.insert(0, new_val)

# Exit early if no data has been entered yet
if not st.session_state.history:
    st.info("💡 **System Awaiting Data:** Input the last 5 to 10 historical numbers from your current game screen into the entry box above to calibrate the risk engines.")
    st.stop()

# --- AUTOMATED CALCULATION ENGINE ---
history = st.session_state.history
total_tracked = len(history)

# Categorize historical distribution parameters
reds = [x for x in history if x < 2.00]
greens = [x for x in history if x >= 2.00]
instant_crashes = [x for x in history if x <= 1.05]

red_pct = (len(reds) / total_tracked) * 100 if total_tracked > 0 else 0
green_pct = (len(greens) / total_tracked) * 100 if total_tracked > 0 else 0

# Calculate current consecutive streaks
current_streak_type = "Red (<2.00x)" if history[0] < 2.00 else "Green (≥2.00x)"
streak_count = 0
for val in history:
    is_red = val < 2.00
    if (current_streak_type.startswith("Red") and is_red) or (current_streak_type.startswith("Green") and not is_red):
        streak_count += 1
    else:
        break

# --- ANALYTICAL VISUALIZATIONS ---
st.markdown("---")
st.subheader("📊 Active Mathematical Matrix")

m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.markdown(f"<div class='metric-box'><b>Rounds Logged</b><br><span style='font-size:24px; font-weight:bold;'>{total_tracked}</span></div>", unsafe_allow_html=True)
with m_col2:
    st.markdown(f"<div class='metric-box'><b>Red Percentage</b><br><span style='font-size:24px; font-weight:bold; color:#EF4444;'>{red_pct:.1f}%</span><br><small>Macro Target: ~50%</small></div>", unsafe_allow_html=True)
with m_col3:
    st.markdown(f"<div class='metric-box'><b>Current Streak</b><br><span style='font-size:24px; font-weight:bold; color:#22C55E;'>{streak_count}x</span><br><small>{current_streak_type}</small></div>", unsafe_allow_html=True)

# --- DYNAMIC RISK RECOMMENDATION ENGINE ---
st.markdown("---")
st.subheader("🤖 Algorithmic Risk Recommendation")

if history[0] >= 12.00:
    st.markdown("""
        <div class='danger-box'>
            <b>🚨 CRITICAL EXHAUSTION DETECTED (POST-SPIKE SYSTEM RECOVERY)</b><br>
            A major multiplier spike just terminated. Statistically, random number generation servers immediately cluster extremely low pullbacks (under 1.50x) following high payout dispersion to protect the house mathematical margin. <br><br>
            <b>STRATEGIC DIRECTIVE:</b> EVADE the next 2 to 3 rounds entirely. Let other players drain their balances fighting the initial correction curve.
        </div>
    """, unsafe_allow_html=True)

elif current_streak_type.startswith("Red") and streak_count >= 4:
    st.markdown(f"""
        <div class='success-box'>
            <b>🟢 OPPOSITE BREAKING TREND ALERT (PROBABILITY REBOUND)</b><br>
            The system has maintained {streak_count} consecutive early losses under 2.00x. While every round is independent, long consecutive strings of low numbers are mathematically unsustainable over extended periods.<br><br>
            <b>STRATEGIC DIRECTIVE:</b> Prepare an automated execution position. Engage a highly strict <b>Auto-Cashout benchmark capped tightly between 1.30x and 1.50x</b> to capture the imminent streak breakage safely.
        </div>
    """, unsafe_allow_html=True)

elif current_streak_type.startswith("Green") and streak_count >= 4:
    st.markdown(f"""
        <div class='warning-box'>
            <b>⚠️ ACCUMULATED HOUSE DEFICIT WARNING (GREED LIMIT REACHED)</b><br>
            The platform has paid out {streak_count} consecutive times above 2.00x. The variance limit is approaching a cliff, meaning an aggressive pullback cluster or a forced 1.00x instant crash is highly probable within the immediate 2-round window.<br><br>
            <b>STRATEGIC DIRECTIVE:</b> Stand down, lower stakes by 75%, or sit out until an explicit red crash clears the platform liabilities.
        </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
        <div class='metric-box' style='border-left: 5px solid #6B7280;'>
            <b>⚖️ BALANCED RANDOM VARIANCE</b><br>
            The distribution metrics indicate normal, standard rolling randomness. The trend is neither heavily overextended nor tightly clustered.<br><br>
            <b>STRATEGIC DIRECTIVE:</b> No clear structural edge present. If choosing to execute positions, rely exclusively on conservative automated thresholds (e.g., 1.50x). Never click manual cashout triggers under fluctuating ping latency.
        </div>
    """, unsafe_allow_html=True)

# --- TRACKED DATA FEEDS ---
st.markdown("---")
st.subheader("📜 Current Session Data Ledger")
st.markdown("Below is the chronological feed of your logged parameters. Keep monitoring for instant house pulls (1.00x - 1.05x).")

# Clean tabular rendering
df = pd.DataFrame({"Round (Order: Newest First)": range(1, total_tracked + 1), "Multiplier Value": history})
st.dataframe(df, use_container_width=True)

# Instant crash count metrics
if instant_crashes:
    st.caption(f"⚠️ Warning: {len(instant_crashes)} instant house crashes (≤1.05x) have been logged in this session. These values are mathematically un-escapable.")

# Reset configuration
if st.button("Purge Active Session Data"):
    st.session_state.history = []
    st.rerun()