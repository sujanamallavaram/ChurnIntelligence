"""
Churn Insight & Intervention Portal v2.2
Enhanced UI with Bright Colors, High Contrast & Professional Design
"""

import streamlit as st
import pandas as pd
import numpy as np

from config import (
    PAGE_CONFIG,
    COLORS,
    CHURN_PROBABILITY_DEFAULT,
    CHURN_PROBABILITY_MIN,
    CHURN_PROBABILITY_MAX,
    CHURN_PROBABILITY_STEP,
    USAGE_VELOCITY_DEFAULT,
    USAGE_VELOCITY_MIN,
    USAGE_VELOCITY_MAX,
    USAGE_VELOCITY_STEP,
    CUSTOMER_SEGMENTS,
)
from data_utils import (
    load_synthetic_churn_data,
    filter_data,
    calculate_kpis,
    get_at_risk_customers,
    get_segment_analysis,
    get_churn_trend_by_tenure,
    get_login_activity_analysis,
    simulate_usage_velocity_impact,
)
from viz_utils import (
    create_kpi_card,
    create_churn_risk_distribution,
    create_segment_churn_comparison,
    create_tenure_churn_trend,
    create_login_activity_impact,
    create_mrr_at_risk_breakdown,
    create_at_risk_priority_matrix,
    create_intervention_impact_gauge,
    create_velocity_impact_table,
)

# Page configuration
st.set_page_config(**PAGE_CONFIG)

# Remove default menu and footer
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Enhanced CSS with Bright Colors & High Contrast
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Poppins:wght@600;700;800&display=swap');

    * {
        margin: 0;
        padding: 0;
    }

    html, body {
        background: linear-gradient(135deg, #F0F4FF 0%, #E8F1FF 50%, #F0E6FF 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        min-height: 100vh;
    }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #F0F4FF 0%, #E8F1FF 50%, #F0E6FF 100%);
    }

    [data-testid="stMainBlockContainer"] {
        padding: 2.5rem 1.5rem;
    }

    h1 {
        background: linear-gradient(135deg, #0052CC 0%, #0080FF 50%, #00B4FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Poppins', sans-serif;
        font-size: 48px;
        font-weight: 800;
        margin-bottom: 12px;
        letter-spacing: -1.5px;
    }

    h2 {
        background: linear-gradient(135deg, #0052CC 0%, #7C3AED 50%, #D946EF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Poppins', sans-serif;
        font-size: 28px;
        font-weight: 700;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    h3 {
        color: #1F2937;
        font-family: 'Inter', sans-serif;
        font-size: 18px;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    /* Sidebar - Bright & Professional */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F5F8FF 100%);
        border-right: 3px solid #0052CC;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #1F2937;
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        background: linear-gradient(135deg, #0052CC, #0080FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    [data-testid="stSidebar"] label {
        color: #1F2937 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }

    /* Enhanced Control Boxes */
    .control-box {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFF 100%);
        padding: 18px;
        border-radius: 14px;
        margin: 18px 0;
        border-left: 4px solid;
        box-shadow: 0 4px 12px rgba(0, 82, 204, 0.08);
        transition: all 0.3s ease;
    }

    .control-box:hover {
        box-shadow: 0 8px 20px rgba(0, 82, 204, 0.15);
        transform: translateX(4px);
    }

    .control-box-blue {
        border-left-color: #0052CC;
    }

    .control-box-orange {
        border-left-color: #FF8C00;
    }

    .control-box-green {
        border-left-color: #00B86B;
    }

    .control-title {
        color: #0052CC;
        font-weight: 700;
        font-size: 14px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .control-description {
        color: #4B5563;
        font-size: 12px;
        line-height: 1.5;
        font-weight: 500;
    }

    /* Slider Styling - HIGH CONTRAST */
    [data-testid="stSlider"] {
        padding: 20px 0;
    }

    [data-testid="stSlider"] [role="slider"] {
        background: linear-gradient(135deg, #0052CC, #00B4FF) !important;
        height: 8px !important;
        border-radius: 4px !important;
    }

    [data-testid="stSlider"] [role="slider"]::before {
        content: '0.10';
        position: absolute;
        left: -20px;
        top: 15px;
        color: #0052CC;
        font-weight: 700;
        font-size: 12px;
    }

    [data-testid="stSlider"] [role="slider"]::after {
        content: '0.90';
        position: absolute;
        right: -20px;
        top: 15px;
        color: #0052CC;
        font-weight: 700;
        font-size: 12px;
    }

    /* Slider Numbers Visible */
    .stSlider > label::before {
        content: attr(data-testid);
        color: #0052CC;
        font-weight: 700;
        font-size: 13px;
    }

    /* Metric Cards - Premium Style */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 8px 24px rgba(0, 82, 204, 0.12) !important;
        border: 2px solid #E5EEFF !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    [data-testid="metric-container"]:hover {
        transform: translateY(-10px) !important;
        box-shadow: 0 16px 40px rgba(0, 82, 204, 0.2) !important;
        border-color: #0052CC !important;
    }

    [data-testid="metric-label"] {
        color: #4B5563 !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
    }

    [data-testid="metric-value"] {
        color: #0052CC !important;
        font-weight: 900 !important;
        font-size: 36px !important;
        font-family: 'Poppins', sans-serif !important;
    }

    [data-testid="metric-delta"] {
        color: #FF8C00 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }

    /* Plotly Charts */
    [data-testid="stPlotlyChart"] {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 82, 204, 0.1);
        background: white;
        padding: 16px;
        border: 1px solid #E5EEFF;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0, 82, 204, 0.08);
        border: 1px solid #E5EEFF;
    }

    /* Column Container */
    [data-testid="column"] {
        padding: 0 10px;
    }

    /* Section Divider */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #0052CC, transparent);
        margin: 3rem 0;
        border: none;
        opacity: 0.5;
    }

    /* Button Styling */
    button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        background: linear-gradient(135deg, #0052CC, #0080FF) !important;
        color: white !important;
        border: none !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
    }

    button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 28px rgba(0, 82, 204, 0.35) !important;
    }

    /* Info/Warning Boxes */
    .info-box {
        background: linear-gradient(135deg, #E3F2FD, #EBF5FF);
        border-left: 5px solid #0052CC;
        padding: 18px;
        border-radius: 12px;
        margin: 18px 0;
        box-shadow: 0 4px 12px rgba(0, 82, 204, 0.1);
    }

    .info-box strong {
        color: #0052CC;
        font-weight: 700;
    }

    .info-box p, .info-box div {
        color: #1F2937;
        font-weight: 500;
    }

    .success-box {
        background: linear-gradient(135deg, #E8F5E9, #F1F8E9);
        border-left: 5px solid #00B86B;
        padding: 18px;
        border-radius: 12px;
        margin: 18px 0;
        box-shadow: 0 4px 12px rgba(0, 184, 107, 0.1);
    }

    .warning-box {
        background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
        border-left: 5px solid #FF8C00;
        padding: 18px;
        border-radius: 12px;
        margin: 18px 0;
        box-shadow: 0 4px 12px rgba(255, 140, 0, 0.1);
    }

    /* Text styles */
    .highlight {
        background: linear-gradient(120deg, #0052CC, #00B4FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #F0F4FF;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #0052CC, #00B4FF);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #0040A0, #0090D0);
    }

    /* Subtitle text */
    .subtitle {
        font-size: 15px;
        color: #4B5563;
        font-weight: 500;
        margin: 8px 0 0 0;
    }

    /* Data info box */
    .data-info {
        background: linear-gradient(135deg, #E3F2FD, #F3E5F5);
        padding: 14px;
        border-radius: 10px;
        margin-top: 24px;
        border: 2px solid #0052CC;
    }

</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if "df" not in st.session_state:
        st.session_state.df = load_synthetic_churn_data(n_records=5000)
    if "churn_probability_threshold" not in st.session_state:
        st.session_state.churn_probability_threshold = CHURN_PROBABILITY_DEFAULT
    if "selected_segments" not in st.session_state:
        st.session_state.selected_segments = CUSTOMER_SEGMENTS.copy()
    if "usage_velocity" not in st.session_state:
        st.session_state.usage_velocity = USAGE_VELOCITY_DEFAULT


def render_sidebar():
    """Render enhanced sidebar with professional design."""
    st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 32px; padding: 20px 0;">
        <h2 style="color: #0052CC; font-size: 28px; margin: 0; font-family: 'Poppins', sans-serif;">🎮 MISSION CONTROL</h2>
        <p style="color: #4B5563; margin: 10px 0 0 0; font-size: 13px; font-weight: 600;">Fine-tune your retention strategy</p>
    </div>
    """, unsafe_allow_html=True)

    # Churn Probability Threshold
    st.sidebar.markdown("""
    <div class="control-box control-box-blue">
        <div class="control-title">📊 CHURN THRESHOLD</div>
        <div class="control-description">Adjust risk sensitivity • 0.1 catches everyone • 0.9 focuses on critical cases</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        churn_probability_threshold = st.slider(
            "Threshold:",
            min_value=CHURN_PROBABILITY_MIN,
            max_value=CHURN_PROBABILITY_MAX,
            value=CHURN_PROBABILITY_DEFAULT,
            step=CHURN_PROBABILITY_STEP,
            label_visibility="collapsed",
            help="Lower = wider net | Higher = focused",
        )
    with col2:
        st.markdown(f"<div style='color: #0052CC; font-weight: 800; font-size: 18px; text-align: center; margin-top: 28px;'>{churn_probability_threshold:.2f}</div>", unsafe_allow_html=True)

    # Customer Segment Filter
    st.sidebar.markdown("""
    <div class="control-box control-box-orange">
        <div class="control-title">👥 SEGMENT FOCUS</div>
        <div class="control-description">Select segments to analyze • Filter updates all insights</div>
    </div>
    """, unsafe_allow_html=True)

    selected_segments = st.sidebar.multiselect(
        "Choose segments:",
        CUSTOMER_SEGMENTS,
        default=CUSTOMER_SEGMENTS,
        label_visibility="collapsed",
    )

    if not selected_segments:
        selected_segments = CUSTOMER_SEGMENTS
        st.sidebar.warning("⚠️ Select at least one segment!")

    # Usage Velocity Multiplier
    st.sidebar.markdown("""
    <div class="control-box control-box-green">
        <div class="control-title">⚡ ENGAGEMENT VELOCITY</div>
        <div class="control-description">Simulate activity changes • See real-time impact on churn</div>
    </div>
    """, unsafe_allow_html=True)

    col3, col4 = st.sidebar.columns([3, 1])
    with col3:
        usage_velocity = st.slider(
            "Velocity:",
            min_value=USAGE_VELOCITY_MIN,
            max_value=USAGE_VELOCITY_MAX,
            value=USAGE_VELOCITY_DEFAULT,
            step=USAGE_VELOCITY_STEP,
            label_visibility="collapsed",
            help="1.0 = normal | 2.0 = double activity",
        )
    with col4:
        st.markdown(f"<div style='color: #00B86B; font-weight: 800; font-size: 18px; text-align: center; margin-top: 28px;'>{usage_velocity:.1f}x</div>", unsafe_allow_html=True)

    st.sidebar.markdown("<div style='height: 3px; background: linear-gradient(90deg, #0052CC, #00B86B); margin: 24px 0; border-radius: 2px;'></div>", unsafe_allow_html=True)

    # Data Info
    st.sidebar.markdown("""
    <div class="data-info">
        <div style="color: #0052CC; font-weight: 700; font-size: 13px; margin-bottom: 10px;">📈 DATASET METRICS</div>
        <div style="color: #1F2937; font-size: 12px; line-height: 1.8; font-weight: 500;">
            <strong style="color: #0052CC;">5,000</strong> active customers<br>
            <strong style="color: #FF8C00;">4</strong> business segments<br>
            <strong style="color: #00B86B;">Real-time</strong> analysis<br>
            <strong style="color: #7C3AED;">100%</strong> interactive
        </div>
    </div>
    """, unsafe_allow_html=True)

    return churn_probability_threshold, selected_segments, usage_velocity


def render_header():
    """Render enhanced header."""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 36px; padding-bottom: 24px; border-bottom: 3px solid #E5EEFF;">
        <h1>🚀 Churn Intelligence Command Center</h1>
        <p class="subtitle">
            <span style="color: #0052CC; font-weight: 700;">Real-time Analytics</span> •
            <span style="color: #FF8C00; font-weight: 700;">Predictive Insights</span> •
            <span style="color: #00B86B; font-weight: 700;">Intervention Actions</span>
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_kpi_section(kpis: dict):
    """Render KPI cards."""
    st.markdown("## 📊 Business Pulse")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="👥 Total Customers",
            value=f"{kpis['total_customers']:,}",
            delta="All accounts",
            delta_color="normal"
        )

    with col2:
        st.metric(
            label="🚨 At Risk",
            value=f"{kpis['at_risk_customers']:,}",
            delta=f"{kpis['at_risk_percentage']:.1f}%",
            delta_color="inverse"
        )

    with col3:
        st.metric(
            label="💰 Total MRR",
            value=f"${kpis['total_mrr']:,.0f}",
            delta="+3.2%",
            delta_color="normal"
        )

    with col4:
        st.metric(
            label="⚠️ MRR at Risk",
            value=f"${kpis['at_risk_mrr']:,.0f}",
            delta=f"{kpis['at_risk_mrr_percentage']:.1f}%",
            delta_color="inverse"
        )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)


def render_analytics_section(filtered_df: pd.DataFrame, usage_velocity: float):
    """Render analytics charts."""
    st.markdown("## 📈 Analytics Deep Dive")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            create_churn_risk_distribution(filtered_df, usage_velocity=usage_velocity),
            use_container_width=True,
            key="risk_dist",
        )

    with col2:
        segment_analysis = get_segment_analysis(filtered_df, usage_velocity=usage_velocity)
        st.plotly_chart(
            create_segment_churn_comparison(segment_analysis),
            use_container_width=True,
            key="segment_comparison",
        )

    col3, col4 = st.columns(2)
    with col3:
        tenure_analysis = get_churn_trend_by_tenure(filtered_df, usage_velocity=usage_velocity)
        st.plotly_chart(
            create_tenure_churn_trend(tenure_analysis),
            use_container_width=True,
            key="tenure_trend",
        )

    with col4:
        login_analysis = get_login_activity_analysis(filtered_df, usage_velocity=usage_velocity)
        st.plotly_chart(
            create_login_activity_impact(login_analysis),
            use_container_width=True,
            key="login_impact",
        )

    col5, col6 = st.columns(2)
    with col5:
        st.plotly_chart(
            create_mrr_at_risk_breakdown(filtered_df, usage_velocity=usage_velocity),
            use_container_width=True,
            key="mrr_breakdown",
        )

    with col6:
        at_risk_df = get_at_risk_customers(filtered_df, churn_probability_threshold=0.5, usage_velocity=usage_velocity)
        if len(at_risk_df) > 0:
            avg_recovery = at_risk_df["Est. Recovery Rate"].astype(float).mean()
        else:
            avg_recovery = 0.65

        st.plotly_chart(
            create_intervention_impact_gauge(avg_recovery),
            use_container_width=True,
            key="recovery_gauge",
        )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)


def render_intervention_section(filtered_df: pd.DataFrame, churn_probability_threshold: float, usage_velocity: float):
    """Render intervention section."""
    st.markdown("## 🎯 Intervention Playbook")

    at_risk_df = get_at_risk_customers(
        filtered_df,
        churn_probability_threshold=churn_probability_threshold,
        usage_velocity=usage_velocity,
        top_n=100,
    )

    if len(at_risk_df) == 0:
        st.markdown("""
        <div class="success-box">
            <div style="font-size: 20px; font-weight: 700; color: #00B86B; margin-bottom: 8px;">✨ All Clear!</div>
            <div style="color: #1F2937; font-weight: 500;">No customers above the selected threshold. Your retention strategy is working perfectly!</div>
        </div>
        """, unsafe_allow_html=True)
        return

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🚨 At-Risk", len(at_risk_df), f"of {len(filtered_df)}")

    with col2:
        critical = len(at_risk_df[at_risk_df["Priority"] == "Critical"])
        high = len(at_risk_df[at_risk_df["Priority"] == "High"])
        st.metric("🔥 Urgent", f"{critical}+{high}", "need action")

    with col3:
        recovery = at_risk_df["Monthly Charges"].sum() * at_risk_df["Est. Recovery Rate"].astype(float).mean()
        st.metric("💎 Recovery", f"${recovery:,.0f}", "potential")

    st.markdown("---")
    st.markdown("### 📍 Priority Matrix")
    st.plotly_chart(
        create_at_risk_priority_matrix(at_risk_df),
        use_container_width=True,
        key="priority_matrix",
    )

    st.markdown("---")
    st.markdown("### 📋 Recommendations")

    display_df = at_risk_df.copy()
    display_df["Monthly Charges"] = display_df["Monthly Charges"].apply(lambda x: f"${x:,.2f}")
    display_df["Churn Risk"] = display_df["Churn Risk"].apply(lambda x: f"{x:.1%}")
    display_df["Est. Recovery Rate"] = display_df["Est. Recovery Rate"].apply(lambda x: f"{x:.0%}")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Customer ID": st.column_config.TextColumn("Customer ID", width="medium"),
            "Segment": st.column_config.TextColumn("Segment", width="small"),
            "Monthly Charges": st.column_config.TextColumn("MRR", width="small"),
            "Churn Risk": st.column_config.TextColumn("Risk", width="small"),
            "Tenure (Months)": st.column_config.NumberColumn("Tenure", width="small"),
            "Days Since Login": st.column_config.NumberColumn("Inactive", width="medium"),
            "Support Tickets": st.column_config.NumberColumn("Support", width="small"),
            "Intervention Type": st.column_config.TextColumn("Action", width="medium"),
            "Priority": st.column_config.TextColumn("Priority", width="small"),
            "Est. Recovery Rate": st.column_config.TextColumn("Recovery", width="small"),
        },
    )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)


def render_velocity_simulation_section(filtered_df: pd.DataFrame, churn_probability_threshold: float):
    """Render velocity simulation."""
    st.markdown("## ⚡ Velocity Impact Simulator")

    st.markdown("""
    <div class="info-box">
        <strong>💡 How It Works:</strong> Watch how customer engagement changes affect churn in real-time.
        Higher velocity = more active = lower churn risk.
    </div>
    """, unsafe_allow_html=True)

    velocity_impact = simulate_usage_velocity_impact(filtered_df, churn_probability_threshold, velocity_range=(0.5, 2.5))

    st.plotly_chart(
        create_velocity_impact_table(velocity_impact),
        use_container_width=True,
        key="velocity_impact",
    )

    st.markdown("""
    ### 🎯 Key Insights

    - **📉 Low Activity (0.5x)**: Disengaged customers → Churn spikes significantly
    - **➡️ Normal (1.0x)**: Baseline state → Current business metrics
    - **📈 High Activity (2.5x)**: Engaged customers → Churn drops dramatically

    **💡 Recommendation**: Invest in engagement campaigns to boost activity levels!
    """)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)


def render_footer():
    """Render footer."""
    st.markdown("""
    <div style="text-align: center; margin-top: 40px; padding: 24px; border-top: 2px solid #E5EEFF; background: linear-gradient(135deg, #F9FAFB, #F0F4FF); border-radius: 12px;">
        <div style="font-weight: 700; color: #0052CC; margin-bottom: 8px; font-size: 16px;">🚀 Churn Intelligence Command Center</div>
        <div style="font-size: 13px; color: #4B5563; font-weight: 500;">
            Powered by real-time analytics • Data-driven decisions • Always learning
        </div>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application logic."""
    initialize_session_state()

    churn_probability_threshold, selected_segments, usage_velocity = render_sidebar()

    filtered_df = filter_data(st.session_state.df, selected_segments)

    kpis = calculate_kpis(
        filtered_df,
        churn_probability_threshold=churn_probability_threshold,
        usage_velocity=usage_velocity,
    )

    render_header()
    render_kpi_section(kpis)
    render_analytics_section(filtered_df, usage_velocity)
    render_intervention_section(filtered_df, churn_probability_threshold, usage_velocity)
    render_velocity_simulation_section(filtered_df, churn_probability_threshold)
    render_footer()


if __name__ == "__main__":
    main()
