"""
Configuration module for Churn Insight & Intervention Portal.
Contains theme settings, color palettes, and global configurations.
"""

# Page Configuration
PAGE_CONFIG = {
    "page_title": "Churn Insight & Intervention Portal",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Color Palette - Professional & Accessible
COLORS = {
    "primary": "#0066CC",          # Professional blue
    "secondary": "#FF6B35",        # Warning orange
    "success": "#00A86B",          # Success green
    "danger": "#DC3545",           # Danger red
    "neutral": "#6C757D",          # Neutral gray
    "background": "#FFFFFF",       # Clean white
    "surface": "#F8F9FA",          # Light gray
    "text_primary": "#1F2937",     # Dark gray
    "text_secondary": "#6B7280",   # Medium gray
}

# Typography
FONT_SIZES = {
    "title": 28,
    "heading": 22,
    "subheading": 18,
    "body": 14,
    "small": 12,
}

# KPI Card Configuration
KPI_CARD_STYLE = """
<style>
.kpi-card {{
    background-color: {bg_color};
    border-left: 4px solid {accent_color};
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}}
.kpi-value {{
    font-size: 32px;
    font-weight: bold;
    color: {accent_color};
    margin: 10px 0;
}}
.kpi-label {{
    font-size: 13px;
    color: #6B7280;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
.kpi-change {{
    font-size: 12px;
    margin-top: 8px;
}}
</style>
"""

# Chart Configuration
CHART_CONFIG = {
    "template": "plotly_white",
    "showlegend": True,
    "hovermode": "x unified",
    "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
}

# Sidebar Configuration
SIDEBAR_CONFIG = {
    "title": "🎛️ Dashboard Controls",
    "filter_sections": ["Churn Probability Threshold", "Customer Segments", "Usage Velocity"],
}

# Data Configuration - Churn Risk Thresholds
CHURN_PROBABILITY_DEFAULT = 0.5
CHURN_PROBABILITY_MIN = 0.1
CHURN_PROBABILITY_MAX = 0.9
CHURN_PROBABILITY_STEP = 0.05

# Usage Velocity Simulation
USAGE_VELOCITY_DEFAULT = 1.0  # 1.0 = normal, <1.0 = less active, >1.0 = more active
USAGE_VELOCITY_MIN = 0.1
USAGE_VELOCITY_MAX = 3.0
USAGE_VELOCITY_STEP = 0.1

# Customer Segments - Real-world business segments
CUSTOMER_SEGMENTS = [
    "Enterprise",
    "Mid-Market",
    "SMB",
    "Personal",
]

# Data Schema (specific columns required)
REQUIRED_COLUMNS = {
    "customer_id": "string",
    "churn_status": "int (0/1)",
    "monthly_charges": "float",
    "tenure": "int (months)",
    "support_tickets_count": "int",
    "last_login_days": "int (days ago)",
    "customer_segment": "string",
}

# Feature Engineering Settings
CHURN_RISK_FACTORS = {
    "tenure": 0.25,                      # Shorter tenure = higher risk
    "last_login_days": 0.25,             # Longer time since login = higher risk
    "support_tickets_count": 0.15,       # Support activity indicator
    "monthly_charges": 0.15,             # Customer value indicator
    "segment_risk": 0.20,                # Segment-based inherent risk
}

# Segment Risk Multipliers
SEGMENT_RISK_MULTIPLIERS = {
    "Enterprise": 0.6,       # Lower risk for enterprise customers
    "Mid-Market": 0.8,       # Moderate risk
    "SMB": 1.0,              # Baseline risk
    "Personal": 1.3,         # Higher risk for personal customers
}

# Intervention Strategy
INTERVENTION_BUDGETS = {
    "Low": 5000,
    "Medium": 15000,
    "High": 50000,
    "Custom": None,
}
