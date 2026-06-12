"""
Visualization utilities for Churn Insight & Intervention Portal.
Contains modular functions for creating professional, interactive Plotly charts.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from config import COLORS, CHART_CONFIG


def create_kpi_card(value, label, change=None, change_label=None, accent_color=None):
    """
    Create an HTML/CSS-based KPI card for dashboard display.
    """
    if accent_color is None:
        accent_color = COLORS["primary"]

    html = f"""
    <div style="
        background-color: {COLORS['surface']};
        border-left: 4px solid {accent_color};
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    ">
        <div style="font-size: 13px; color: #6B7280; text-transform: uppercase; letter-spacing: 0.5px;">
            {label}
        </div>
        <div style="font-size: 32px; font-weight: bold; color: {accent_color}; margin: 10px 0;">
            {value}
        </div>
        {f'<div style="font-size: 12px; color: {accent_color}; margin-top: 8px;">{change_label} {change}</div>' if change is not None else ''}
    </div>
    """
    return html


def create_churn_risk_distribution(df: pd.DataFrame, usage_velocity: float = 1.0) -> go.Figure:
    """
    Create a histogram showing distribution of churn risk scores.
    """
    from data_utils import calculate_churn_risk_scores

    risks = calculate_churn_risk_scores(df, usage_velocity=usage_velocity)

    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=risks,
        nbinsx=30,
        name="Risk Score Distribution",
        marker=dict(
            color=risks,
            colorscale='RdYlGn_r',
            showscale=True,
            colorbar=dict(title="Risk Score", len=0.7),
            line=dict(color="white", width=1)
        ),
        hovertemplate="<b>Risk Range</b><br>Count: %{y}<br>Score: %{x:.2f}<extra></extra>",
    ))

    fig.update_layout(
        title="<b>📊 Churn Risk Distribution</b><br><sub>Customer risk profile across organization</sub>",
        xaxis_title="Churn Risk Score",
        yaxis_title="Number of Customers",
        template=CHART_CONFIG["template"],
        height=400,
        margin=CHART_CONFIG["margin"],
        showlegend=False,
        font=dict(size=11),
        title_font_size=14,
    )

    return fig


def create_segment_churn_comparison(segment_analysis: pd.DataFrame) -> go.Figure:
    """
    Create grouped bar chart comparing churn metrics by segment.
    """
    fig = go.Figure()

    # Customer count
    fig.add_trace(go.Bar(
        x=segment_analysis["customer_segment"],
        y=segment_analysis["Customer Count"],
        name="Customer Count",
        marker=dict(
            color=COLORS["primary"],
            line=dict(color="white", width=2)
        ),
        yaxis="y",
        hovertemplate="<b>%{x}</b><br>👥 Customers: %{y:,}<extra></extra>",
    ))

    # Churn risk (secondary axis)
    fig.add_trace(go.Bar(
        x=segment_analysis["customer_segment"],
        y=segment_analysis["Avg Churn Risk"] * 100,
        name="Avg Churn Risk (%)",
        marker=dict(
            color=COLORS["secondary"],
            line=dict(color="white", width=2)
        ),
        yaxis="y2",
        hovertemplate="<b>%{x}</b><br>⚠️ Risk: %{y:.1f}%<extra></extra>",
    ))

    fig.update_layout(
        title="<b>👥 Segment Performance</b><br><sub>Customer distribution & churn risk by segment</sub>",
        xaxis_title="Customer Segment",
        yaxis_title="Number of Customers",
        yaxis2=dict(
            title="Average Churn Risk (%)",
            overlaying="y",
            side="right",
        ),
        barmode="group",
        template=CHART_CONFIG["template"],
        height=400,
        margin=CHART_CONFIG["margin"],
        hovermode="x unified",
        font=dict(size=11),
        title_font_size=14,
    )

    return fig


def create_tenure_churn_trend(tenure_analysis: pd.DataFrame) -> go.Figure:
    """
    Create a combination chart showing churn trends by customer tenure.
    """
    fig = go.Figure()

    # Churn rate (bar)
    fig.add_trace(go.Bar(
        x=tenure_analysis["tenure_bucket"],
        y=tenure_analysis["Churn Rate"],
        name="Churn Rate (%)",
        marker=dict(
            color=tenure_analysis["Churn Rate"],
            colorscale='Reds',
            showscale=False,
            line=dict(color="white", width=2)
        ),
        yaxis="y",
        hovertemplate="<b>%{x}</b><br>📉 Churn Rate: %{y:.1f}%<extra></extra>",
    ))

    # Average risk (line)
    fig.add_trace(go.Scatter(
        x=tenure_analysis["tenure_bucket"],
        y=tenure_analysis["Avg Risk"] * 100,
        name="Avg Risk Score",
        line=dict(color=COLORS["primary"], width=4),
        mode="lines+markers",
        marker=dict(size=10, color=COLORS["primary"], line=dict(color="white", width=2)),
        fill='tozeroy',
        fillcolor='rgba(0, 102, 204, 0.1)',
        yaxis="y2",
        hovertemplate="<b>%{x}</b><br>📊 Risk: %{y:.1f}%<extra></extra>",
    ))

    fig.update_layout(
        title="<b>📅 Tenure Impact</b><br><sub>How customer lifetime affects churn probability</sub>",
        xaxis_title="Customer Tenure",
        yaxis_title="Churn Rate (%)",
        yaxis2=dict(
            title="Average Churn Risk (%)",
            overlaying="y",
            side="right",
            range=[0, 100],
        ),
        template=CHART_CONFIG["template"],
        height=400,
        margin=CHART_CONFIG["margin"],
        hovermode="x unified",
        font=dict(size=11),
        title_font_size=14,
    )

    return fig


def create_login_activity_impact(login_analysis: pd.DataFrame) -> go.Figure:
    """
    Create a chart showing churn relationship with login recency.
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=login_analysis["login_recency"],
        y=login_analysis["Churn Rate"],
        mode="lines+markers",
        name="Churn Rate (%)",
        line=dict(color=COLORS["danger"], width=3),
        marker=dict(size=10),
        fill="tozeroy",
        fillcolor="rgba(220, 53, 69, 0.1)",
        hovertemplate="<b>%{x}</b><br>Churn Rate: %{y:.1f}%<extra></extra>",
    ))

    fig.update_layout(
        title="Login Activity Impact on Churn (Usage Velocity Shows Real-time Effect)",
        xaxis_title="Days Since Last Login",
        yaxis_title="Churn Rate (%)",
        template=CHART_CONFIG["template"],
        height=400,
        margin=CHART_CONFIG["margin"],
        showlegend=False,
    )

    return fig


def create_mrr_at_risk_breakdown(df: pd.DataFrame, usage_velocity: float = 1.0, threshold: float = 0.5) -> go.Figure:
    """
    Create a pie chart showing MRR breakdown by risk segment.
    """
    from data_utils import calculate_churn_risk_scores

    df_copy = df.copy()
    df_copy["churn_risk"] = calculate_churn_risk_scores(df_copy, usage_velocity=usage_velocity)

    # Segment by risk level
    df_copy["risk_category"] = pd.cut(
        df_copy["churn_risk"],
        bins=[0, 0.33, 0.66, 1.0],
        labels=["Low Risk", "Medium Risk", "High Risk"],
    )

    mrr_by_risk = df_copy.groupby("risk_category")["monthly_charges"].sum()

    colors_map = {
        "Low Risk": COLORS["success"],
        "Medium Risk": COLORS["secondary"],
        "High Risk": COLORS["danger"],
    }

    fig = go.Figure(data=[go.Pie(
        labels=mrr_by_risk.index,
        values=mrr_by_risk.values,
        marker=dict(
            colors=[colors_map.get(label, COLORS["neutral"]) for label in mrr_by_risk.index],
            line=dict(color="white", width=2),
        ),
        textposition="inside",
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>MRR: $%{value:,.0f}<extra></extra>",
    )])

    fig.update_layout(
        title="Monthly Recurring Revenue by Risk Level",
        height=400,
        margin=CHART_CONFIG["margin"],
    )

    return fig


def create_at_risk_priority_matrix(at_risk_df: pd.DataFrame) -> go.Figure:
    """
    Create a scatter plot showing at-risk customers by MRR and churn risk.
    """
    if len(at_risk_df) == 0:
        fig = go.Figure()
        fig.add_annotation(text="No at-risk customers at this threshold")
        return fig

    # Create priority color mapping
    priority_colors = {
        "Critical": COLORS["danger"],
        "High": COLORS["secondary"],
        "Medium": COLORS["primary"],
        "Low": COLORS["success"],
    }

    fig = go.Figure()

    for priority in ["Critical", "High", "Medium", "Low"]:
        data = at_risk_df[at_risk_df["Priority"] == priority]
        if len(data) == 0:
            continue

        fig.add_trace(go.Scatter(
            x=data["Monthly Charges"],
            y=data["Churn Risk"],
            mode="markers",
            name=priority,
            marker=dict(
                size=8,
                color=priority_colors.get(priority, COLORS["neutral"]),
                opacity=0.7,
                line=dict(width=1, color="white"),
            ),
            text=data["Customer ID"],
            customdata=data[["Segment", "Tenure (Months)", "Days Since Login"]],
            hovertemplate=(
                "<b>%{text}</b><br>"
                "MRR: $%{x:,.0f}<br>"
                "Risk: %{y:.1%}<br>"
                "Segment: %{customdata[0]}<br>"
                "Tenure: %{customdata[1]} mo<br>"
                "Inactive: %{customdata[2]} days"
                "<extra></extra>"
            ),
        ))

    fig.update_layout(
        title="At-Risk Customers: Priority Matrix (MRR vs Churn Risk)",
        xaxis_title="Monthly Recurring Revenue ($)",
        yaxis_title="Churn Risk Score",
        template=CHART_CONFIG["template"],
        height=450,
        margin=CHART_CONFIG["margin"],
        hovermode="closest",
    )

    return fig


def create_intervention_impact_gauge(recovery_rate: float, target: float = 0.65) -> go.Figure:
    """
    Create a gauge chart showing estimated recovery potential.
    """
    color = COLORS["success"] if recovery_rate >= target else COLORS["secondary"]

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=recovery_rate * 100,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Avg Recovery Potential"},
        delta={"reference": target * 100, "suffix": "%"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": color},
            "steps": [
                {"range": [0, 33], "color": COLORS["danger"]},
                {"range": [33, 66], "color": COLORS["secondary"]},
                {"range": [66, 100], "color": COLORS["success"]},
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": target * 100,
            },
        },
    ))

    fig.update_layout(height=350, margin=CHART_CONFIG["margin"])

    return fig


def create_velocity_impact_table(velocity_impact_df: pd.DataFrame) -> go.Figure:
    """
    Create a table showing impact of usage velocity on churn metrics.
    """
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(velocity_impact_df.columns),
            fill_color=COLORS["primary"],
            align="center",
            font=dict(color="white", size=12),
        ),
        cells=dict(
            values=[velocity_impact_df[col] for col in velocity_impact_df.columns],
            fill_color="lavender",
            align="center",
            font=dict(size=11),
        ),
    )])

    fig.update_layout(
        title="Impact of Usage Velocity on Churn Metrics",
        height=400,
        margin=CHART_CONFIG["margin"],
    )

    return fig
