"""
🌙 Midnight Cart: Executive Operations Simulator
Author: Senior Consulting Team (IIT Roorkee × Masai 2026)
Run: streamlit run src/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

st.set_page_config(
    page_title="Midnight Cart: Executive Ops Cockpit",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #1E293B;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #38BDF8;
        margin-bottom: 10px;
    }
    .metric-title { color: #94A3B8; font-size: 0.85rem; font-weight: 600; }
    .metric-val { color: #F8FAFC; font-size: 1.6rem; font-weight: 700; }
    .metric-sub { color: #38BDF8; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("src/clean_orders.csv")
    return df

@st.cache_resource
def load_model(df):
    num_features = ['items_count', 'basket_value_inr', 'discount_inr', 'rain_mm', 'riders_on_duty', 'eta_shown_min']
    cat_features = ['payment_mode', 'coupon_code', 'is_first_order', 'exam_week', 'zone', 'top_category', 'is_late_night']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_features),
            ('cat', OneHotEncoder(drop='first', sparse_output=False), cat_features)
        ]
    )
    
    clf = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42))
    ])
    
    X = df[num_features + cat_features]
    y = df['cancelled'].astype(int)
    clf.fit(X, y)
    return clf

df = load_data()
model = load_model(df)

# Header
st.title("🌙 Midnight Cart: Executive Operations Simulator")
st.caption("City Operations Head Command Cockpit · Rohan Mehta · IIT Roorkee × Masai Immersion 2026")

# Top KPI Banner
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""<div class="metric-card">
        <div class="metric-title">90-DAY REALISED PROFIT</div>
        <div class="metric-val">₹78,183</div>
        <div class="metric-sub">Across 2,291 delivered orders</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="metric-card">
        <div class="metric-title">TOTAL CANCELLATION LOSS</div>
        <div class="metric-val">₹10,255</div>
        <div class="metric-sub">The theoretical profit ceiling</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="metric-card">
        <div class="metric-title">11 PM CANCELLATION SPIKE</div>
        <div class="metric-val">40.0%</div>
        <div class="metric-sub">Shoots to 71.2% in Exam Week</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown("""<div class="metric-card">
        <div class="metric-title">PROJECTED STRATEGY LIFT</div>
        <div class="metric-val">+₹11,674</div>
        <div class="metric-sub">+14.9% Net Profit Expansion</div>
    </div>""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "⚡ 1. The 11 PM Fleet Simulator",
    "🎟️ 2. Coupon Unit Economics",
    "🎯 3. Live Checkout Risk Scorer",
    "📊 4. Historical Data Explorer"
])

# ----------------- TAB 1: FLEET SIMULATOR -----------------
with tab1:
    st.subheader("Shift-Staggering & Fleet Reallocation (The 11 PM Fix)")
    st.write("Simulate the impact of re-timing afternoon idle riders to the midnight rush without adding new headcount.")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("### Operational Controls")
        sim_riders = st.slider("Active Riders on Duty at 23:00", min_value=3, max_value=9, value=8, step=1)
        sim_exam = st.checkbox("Exam Week Active?", value=True)
        sim_rain = st.slider("Rainfall (mm)", min_value=0.0, max_value=12.0, value=0.0, step=0.5)
        
        # Empirical interpolation based on historical data
        # At 3.9 riders -> ETA 20.1 min, Cancel Rate 40% (71% in exam)
        # At 8 riders -> ETA 13.7 min, Cancel Rate 8% (18% in exam)
        eta_est = max(11.0, 20.1 - (sim_riders - 3.9) * 1.5 + (sim_rain * 0.4))
        if sim_exam:
            cancel_est = max(14.0, 71.2 - (sim_riders - 3.9) * 12.8 + (sim_rain * 1.5))
        else:
            cancel_est = max(8.0, 40.0 - (sim_riders - 3.9) * 7.5 + (sim_rain * 1.5))
            
        st.markdown("---")
        st.metric("Predicted Quoted ETA", f"{eta_est:.1f} mins", delta=f"{eta_est - 20.1:.1f} mins", delta_color="inverse")
        st.metric("Predicted Cancellation Rate", f"{cancel_est:.1f}%", delta=f"{cancel_est - (71.2 if sim_exam else 40.0):.1f}%", delta_color="inverse")
    
    with c2:
        # Comparison Chart
        hours = list(range(10, 24)) + [0, 1]
        hour_labels = [f"{h}:00" for h in hours]
        baseline_cancels = df.groupby('order_hour')['cancelled'].mean() * 100
        
        sim_series = baseline_cancels.copy()
        sim_series[23] = cancel_est
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=hour_labels, 
            y=[baseline_cancels.get(h, 10) for h in hours],
            name="Current Baseline Cancel %",
            marker_color="#EF4444"
        ))
        fig.add_trace(go.Scatter(
            x=hour_labels,
            y=[sim_series.get(h, 10) for h in hours],
            name="Simulated Post-Shift Rate",
            line=dict(color="#10B981", width=3, dash="dot"),
            mode="lines+markers"
        ))
        fig.update_layout(
            title="Hourly Cancellation Rate: Current vs. Simulated Roster",
            xaxis_title="Hour of Day",
            yaxis_title="Cancellation Rate (%)",
            template="plotly_dark",
            height=380
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Financial Impact Box
        orders_saved_90d = int(70 * ((71.2 - cancel_est) / 53.0)) if sim_exam else int(45 * ((40.0 - cancel_est) / 32.0))
        recovered_margin = orders_saved_90d * 245 * 0.145
        st.info(f"💡 **Rohan's ROI:** Keeping **{sim_riders} riders** at 23:00 recovers **~{orders_saved_90d} cancelled orders** and adds **+₹{recovered_margin:,.0f} gross margin** over 90 days with **₹0 added headcount cost**.")

# ----------------- TAB 2: COUPON SIMULATOR -----------------
with tab2:
    st.subheader("Coupon Economics: Stopping the FIRST50 Cash Bleed")
    st.write("Analyze how restructuring `FIRST50` eliminates negative contribution margins.")
    
    col_a, col_b = st.columns([1, 2])
    with col_a:
        mov_choice = st.slider("Minimum Order Value (MOV) for FIRST50 (₹)", min_value=0, max_value=250, value=199, step=10)
        coupon_mode = st.radio("Discount Structure", [
            "Fixed ₹40 OFF (Proposed)",
            "50% OFF up to ₹50",
            "Current Unrestricted ₹50 Flat OFF (Legacy)"
        ])
        prepaid_only = st.checkbox("Require Prepaid Payment (Disable COD)?", value=True)
        
        f50_orders = df[df['coupon_code'] == 'FIRST50'].copy()
        if mov_choice > 0:
            qualifying = f50_orders[f50_orders['basket_value_inr'] >= mov_choice]
        else:
            qualifying = f50_orders
            
        if prepaid_only:
            qualifying = qualifying[qualifying['payment_mode'] != 'COD']
            
        st.metric("Eligible Orders (out of 354)", f"{len(qualifying)}")
        
    with col_b:
        # Compute economics
        if "Fixed ₹40" in coupon_mode:
            disc_est = 40.0
        elif "50%" in coupon_mode:
            disc_est = qualifying['basket_value_inr'].apply(lambda b: min(50.0, b * 0.50)).mean() if len(qualifying) > 0 else 0
        else:
            disc_est = 50.0
            
        avg_basket = qualifying['basket_value_inr'].mean() if len(qualifying) > 0 else 188.0
        avg_margin_pct = qualifying['margin_pct'].mean() if len(qualifying) > 0 else 14.5
        gross_profit_per_order = avg_basket * (avg_margin_pct / 100.0)
        net_profit_per_order = gross_profit_per_order - disc_est
        total_net_profit = net_profit_per_order * len(qualifying)
        
        # Comparison Bar
        comp_df = pd.DataFrame({
            "Scenario": ["Legacy FIRST50 (Reality)", "Restructured Proposal"],
            "Net Profit (₹)": [-4587, total_net_profit]
        })
        fig2 = px.bar(
            comp_df, x="Scenario", y="Net Profit (₹)",
            color="Net Profit (₹)",
            color_continuous_scale=["#EF4444", "#10B981"],
            text_auto=True,
            title="90-Day Coupon Net Profit: Legacy vs. Restructured"
        )
        fig2.update_layout(template="plotly_dark", height=320)
        st.plotly_chart(fig2, use_container_width=True)
        
        st.success(f"🎉 **Net Profit Swing:** Moving to MOV ₹{mov_choice} ({coupon_mode}) creates a **+₹{total_net_profit - (-4587):,.0f} direct bottom-line recovery**.")

# ----------------- TAB 3: CHECKOUT RISK SCORER -----------------
with tab3:
    st.subheader("Live Checkout Risk Scorer (Machine Learning Inference)")
    st.write("Real-time cancellation probability prediction based on our leakage-free Logistic Regression model.")
    
    rx1, rx2, rx3 = st.columns(3)
    with rx1:
        in_zone = st.selectbox("Hostel Zone", sorted(df['zone'].unique()))
        in_cat = st.selectbox("Product Category", sorted(df['top_category'].unique()))
        in_payment = st.selectbox("Payment Mode", ["UPI", "Card", "COD"])
    with rx2:
        in_basket = st.number_input("Basket Value (₹)", min_value=50, max_value=2000, value=250, step=25)
        in_coupon = st.selectbox("Coupon Code", ["NONE", "FIRST50", "EXAM20"])
        in_first = st.selectbox("Is Customer's First Order?", ["Y", "N"])
    with rx3:
        in_hour = st.slider("Hour of Day", min_value=10, max_value=23, value=23)
        in_exam = st.selectbox("Exam Week?", ["Y", "N"])
        in_rain = st.number_input("Rainfall (mm)", min_value=0.0, max_value=15.0, value=0.0, step=0.5)
        
    # Build single-row DataFrame
    input_df = pd.DataFrame([{
        'items_count': 2,
        'basket_value_inr': in_basket,
        'discount_inr': 50 if in_coupon == 'FIRST50' else (in_basket * 0.2 if in_coupon == 'EXAM20' else 0),
        'rain_mm': in_rain,
        'riders_on_duty': 4 if in_hour in [23, 0, 1] else 7,
        'eta_shown_min': 20 if in_hour in [23, 0, 1] else 13,
        'payment_mode': in_payment,
        'coupon_code': in_coupon,
        'is_first_order': in_first,
        'exam_week': in_exam,
        'zone': in_zone,
        'top_category': in_cat,
        'is_late_night': 1 if in_hour in [23, 0, 1] else 0
    }])
    
    pred_prob = model.predict_proba(input_df)[0][1] * 100
    
    st.markdown("---")
    res_col1, res_col2 = st.columns([1, 2])
    with res_col1:
        if pred_prob > 50:
            st.error(f"⚠️ **HIGH CANCELLATION RISK: {pred_prob:.1f}%**")
        elif pred_prob > 25:
            st.warning(f"⚡ **MODERATE RISK: {pred_prob:.1f}%**")
        else:
            st.success(f"✅ **LOW RISK: {pred_prob:.1f}%**")
    with res_col2:
        if in_payment == "COD" and pred_prob > 30:
            st.info("💡 **Recommended Action:** Prompt customer at checkout: *'Pay via UPI to unlock 12-Minute Express Priority Delivery'*. This drops cancellation probability by ~60%!")
        elif in_zone == "Market Road PGs":
            st.info("💡 **Recommended Action:** Add +3 min zone buffer to set realistic delivery expectations and dispatch via perimeter drop-point.")
        else:
            st.info("💡 **Standard Routing:** Route order to the standard dispatch conveyor.")

# ----------------- TAB 4: HISTORICAL EXPLORER -----------------
with tab4:
    st.subheader("Audited Dataset Overview (2,685 Clean Orders)")
    st.dataframe(df[['order_id', 'order_dt', 'zone', 'top_category', 'basket_value_inr', 'coupon_code', 'payment_mode', 'eta_shown_min', 'riders_on_duty', 'cancelled']].head(15), use_container_width=True)
    st.caption("Clean dataset exported from `src/data_pipeline.py`. Excludes 84 duplicates, 15 ghost orders, and imputed 16 zero-rider sensor dropouts.")
