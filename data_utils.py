"""
Data utilities for Churn Insight & Intervention Portal.
Handles data loading, caching, feature engineering, and transformations.
"""

import pandas as pd
import numpy as np
import streamlit as st
from config import (
    CUSTOMER_SEGMENTS,
    CHURN_RISK_FACTORS,
    SEGMENT_RISK_MULTIPLIERS,
)


@st.cache_data
def load_synthetic_churn_data(n_records: int = 5000) -> pd.DataFrame:
    """
    Generate high-quality synthetic customer churn dataset.

    Dataset includes:
    - customer_id: Unique identifier (CUST_000001, CUST_000002, etc.)
    - churn_status: Binary (0=active, 1=churned)
    - monthly_charges: Customer's monthly spend ($)
    - tenure: Months as customer
    - support_tickets_count: Number of support interactions
    - last_login_days: Days since last login
    - customer_segment: Business segment (Enterprise, Mid-Market, SMB, Personal)

    Churn is probabilistically generated based on real-world patterns.
    """
    np.random.seed(42)

    # Customer IDs
    customer_ids = [f"CUST_{i:06d}" for i in range(1, n_records + 1)]

    # Customer segments with distribution
    segment_distribution = np.random.choice(
        CUSTOMER_SEGMENTS,
        size=n_records,
        p=[0.15, 0.25, 0.35, 0.25],  # Enterprise, Mid-Market, SMB, Personal
    )

    # Tenure: Exponential distribution (more newer customers)
    tenure = np.random.exponential(scale=20, size=n_records).astype(int) + 1
    tenure = np.clip(tenure, 1, 120)

    # Monthly charges: Log-normal distribution (more realistic pricing)
    monthly_charges = np.random.lognormal(mean=4.5, sigma=0.8, size=n_records)
    monthly_charges = np.clip(monthly_charges, 9.99, 299.99)

    # Last login: More recent is better
    last_login_days = np.random.exponential(scale=10, size=n_records).astype(int)
    last_login_days = np.clip(last_login_days, 0, 180)

    # Support tickets: Poisson distribution
    support_tickets_count = np.random.poisson(lam=2, size=n_records)

    # Generate churn status based on customer features
    churn_status = np.zeros(n_records, dtype=int)
    churn_probabilities = calculate_churn_probability(
        tenure,
        last_login_days,
        support_tickets_count,
        monthly_charges,
        segment_distribution,
        usage_velocity=1.0,
    )

    churn_status = (np.random.rand(n_records) < churn_probabilities).astype(int)

    # Create DataFrame
    df = pd.DataFrame({
        "customer_id": customer_ids,
        "churn_status": churn_status,
        "monthly_charges": monthly_charges.round(2),
        "tenure": tenure,
        "support_tickets_count": support_tickets_count,
        "last_login_days": last_login_days,
        "customer_segment": segment_distribution,
    })

    # Add derived features for analysis
    df["days_until_annual_renewal"] = np.random.randint(0, 365, n_records)
    df["customer_support_response_time_hours"] = np.random.exponential(scale=4, size=n_records)
    df["total_customer_value"] = (df["monthly_charges"] * df["tenure"]).round(2)
    df["engagement_score"] = (
        (100 - df["last_login_days"]) / 100 * 0.4 +
        (df["support_tickets_count"] / 10 * 0.3) +
        (df["tenure"] / 120 * 0.3)
    ).clip(0, 1)

    return df


def calculate_churn_probability(
    tenure: np.ndarray,
    last_login_days: np.ndarray,
    support_tickets_count: np.ndarray,
    monthly_charges: np.ndarray,
    segments: np.ndarray,
    usage_velocity: float = 1.0,
) -> np.ndarray:
    """
    Calculate churn probability (0-1) for each customer.

    Factors considered:
    1. Tenure: Newer customers have higher churn risk
    2. Last Login: Inactive customers are more likely to churn
    3. Support Activity: May indicate satisfaction issues
    4. Customer Value: Higher spend may reduce churn
    5. Segment: Enterprise less likely to churn than Personal
    6. Usage Velocity: How active the customer is (simulation factor)

    Args:
        tenure: Months as customer
        last_login_days: Days since last login
        support_tickets_count: Number of support interactions
        monthly_charges: Monthly spend
        segments: Customer segment
        usage_velocity: Multiplier for login activity (1.0=normal, >1.0=more active)

    Returns:
        Array of churn probabilities (0-1)
    """
    n = len(tenure)
    churn_prob = np.zeros(n)

    # Base risk from tenure (newer = higher risk)
    tenure_normalized = np.clip(tenure / 120, 0, 1)
    tenure_risk = (1 - tenure_normalized) * CHURN_RISK_FACTORS["tenure"]
    churn_prob += tenure_risk

    # Risk from inactivity (adjusted by usage_velocity)
    login_normalized = np.clip(last_login_days / 180, 0, 1)
    login_risk = login_normalized * CHURN_RISK_FACTORS["last_login_days"] / usage_velocity
    churn_prob += login_risk

    # Support ticket impact (high support = unclear satisfaction)
    support_normalized = np.clip(support_tickets_count / 10, 0, 1)
    support_risk = support_normalized * CHURN_RISK_FACTORS["support_tickets_count"]
    churn_prob += support_risk

    # Customer value protection (higher spend = loyalty)
    value_normalized = np.clip(monthly_charges / 300, 0, 1)
    value_risk = (1 - value_normalized) * CHURN_RISK_FACTORS["monthly_charges"]
    churn_prob += value_risk

    # Segment-based risk multiplier
    segment_risk = np.array([
        SEGMENT_RISK_MULTIPLIERS.get(seg, 1.0) * CHURN_RISK_FACTORS["segment_risk"]
        for seg in segments
    ])
    churn_prob += segment_risk

    # Normalize to 0-1 range using sigmoid-like function
    total_weight = sum(CHURN_RISK_FACTORS.values())
    churn_prob = churn_prob / (total_weight * 1.2)  # Slightly scale down to keep in reasonable range
    churn_prob = 1 / (1 + np.exp(-5 * (churn_prob - 0.5)))  # Sigmoid transformation

    return np.clip(churn_prob, 0, 1)


def filter_data(
    df: pd.DataFrame,
    segments: list,
) -> pd.DataFrame:
    """
    Apply filters to the dataset.

    Args:
        df: Full dataset
        segments: List of customer segments to include

    Returns:
        Filtered DataFrame
    """
    filtered_df = df.copy()

    # Segment filter
    if segments and len(segments) < len(CUSTOMER_SEGMENTS):
        filtered_df = filtered_df[filtered_df["customer_segment"].isin(segments)]

    return filtered_df


def calculate_churn_risk_scores(
    df: pd.DataFrame,
    usage_velocity: float = 1.0,
) -> np.ndarray:
    """
    Calculate individual churn risk scores for all customers.

    Args:
        df: Customer dataset
        usage_velocity: Simulation parameter affecting login activity impact

    Returns:
        Array of churn risk scores (0-1)
    """
    return calculate_churn_probability(
        df["tenure"].values,
        df["last_login_days"].values,
        df["support_tickets_count"].values,
        df["monthly_charges"].values,
        df["customer_segment"].values,
        usage_velocity=usage_velocity,
    )


def calculate_kpis(
    df: pd.DataFrame,
    churn_probability_threshold: float = 0.5,
    usage_velocity: float = 1.0,
) -> dict:
    """
    Calculate key performance indicators.

    Args:
        df: Filtered dataset
        churn_probability_threshold: Probability threshold for flagging at-risk
        usage_velocity: Usage velocity multiplier for simulation

    Returns:
        Dictionary of KPI values
    """
    # Calculate churn risk scores with usage velocity
    churn_risks = calculate_churn_risk_scores(df, usage_velocity=usage_velocity)
    df_with_risk = df.copy()
    df_with_risk["churn_risk"] = churn_risks

    # Identify at-risk customers
    at_risk = df_with_risk[df_with_risk["churn_risk"] > churn_probability_threshold]
    churned = df[df["churn_status"] == 1]

    total_customers = len(df)
    at_risk_customers = len(at_risk)
    at_risk_percentage = (at_risk_customers / total_customers * 100) if total_customers > 0 else 0

    total_mrr = df["monthly_charges"].sum()
    at_risk_mrr = at_risk["monthly_charges"].sum() if len(at_risk) > 0 else 0
    at_risk_mrr_percentage = (at_risk_mrr / total_mrr * 100) if total_mrr > 0 else 0

    return {
        "total_customers": total_customers,
        "at_risk_customers": at_risk_customers,
        "at_risk_percentage": at_risk_percentage,
        "avg_churn_risk": churn_risks.mean(),
        "churned_count": len(churned),
        "churn_rate_actual": (len(churned) / total_customers * 100) if total_customers > 0 else 0,
        "total_mrr": total_mrr,
        "at_risk_mrr": at_risk_mrr,
        "at_risk_mrr_percentage": at_risk_mrr_percentage,
    }


def get_at_risk_customers(
    df: pd.DataFrame,
    churn_probability_threshold: float = 0.5,
    usage_velocity: float = 1.0,
    top_n: int = 100,
) -> pd.DataFrame:
    """
    Get list of at-risk customers with intervention recommendations.

    Args:
        df: Customer dataset
        churn_probability_threshold: Probability threshold
        usage_velocity: Usage velocity multiplier
        top_n: Number of top at-risk customers to return

    Returns:
        DataFrame with at-risk customers and recommendations
    """
    df_copy = df.copy()
    df_copy["churn_risk"] = calculate_churn_risk_scores(df_copy, usage_velocity=usage_velocity)

    # Filter to at-risk customers
    at_risk = df_copy[df_copy["churn_risk"] > churn_probability_threshold].copy()

    if len(at_risk) == 0:
        return pd.DataFrame()

    # Sort by risk and customer value
    at_risk["risk_value_score"] = (
        at_risk["churn_risk"] * (at_risk["monthly_charges"] / at_risk["monthly_charges"].max())
    )
    at_risk = at_risk.sort_values("risk_value_score", ascending=False)

    # Generate intervention recommendations
    at_risk["intervention_type"] = at_risk.apply(_determine_intervention, axis=1)
    at_risk["priority"] = at_risk.apply(_determine_priority, axis=1)
    at_risk["estimated_recovery_rate"] = at_risk.apply(_estimate_recovery, axis=1)

    # Select columns for display
    result = at_risk.head(top_n)[[
        "customer_id",
        "customer_segment",
        "monthly_charges",
        "churn_risk",
        "tenure",
        "last_login_days",
        "support_tickets_count",
        "intervention_type",
        "priority",
        "estimated_recovery_rate",
    ]].copy()

    result.columns = [
        "Customer ID",
        "Segment",
        "Monthly Charges",
        "Churn Risk",
        "Tenure (Months)",
        "Days Since Login",
        "Support Tickets",
        "Intervention Type",
        "Priority",
        "Est. Recovery Rate",
    ]

    return result


def _determine_intervention(row: pd.Series) -> str:
    """Determine intervention type based on customer profile."""
    risk = row["churn_risk"]
    tenure = row["tenure"]
    last_login = row["last_login_days"]
    support = row["support_tickets_count"]
    charges = row["monthly_charges"]

    if risk > 0.8 and charges > 100:
        return "Executive Outreach"
    elif last_login > 60:
        return "Re-Engagement Campaign"
    elif support > 5:
        return "Support Enhancement"
    elif tenure < 6:
        return "Onboarding Follow-up"
    else:
        return "Retention Offer"


def _determine_priority(row: pd.Series) -> str:
    """Determine intervention priority."""
    risk = row["churn_risk"]
    charges = row["monthly_charges"]

    if risk > 0.75 and charges > 100:
        return "Critical"
    elif risk > 0.65 or charges > 150:
        return "High"
    elif risk > 0.5:
        return "Medium"
    else:
        return "Low"


def _estimate_recovery(row: pd.Series) -> float:
    """Estimate probability of successful recovery."""
    risk = row["churn_risk"]
    tenure = row["tenure"]

    base_recovery = 0.6
    tenure_adjustment = (tenure / 120) * 0.2  # Longer tenure = easier to recover
    risk_adjustment = (1 - risk) * 0.2  # Lower risk = easier to recover

    return np.clip(base_recovery + tenure_adjustment + risk_adjustment, 0.1, 0.9)


def get_segment_analysis(df: pd.DataFrame, usage_velocity: float = 1.0) -> pd.DataFrame:
    """
    Analyze churn metrics by customer segment.

    Args:
        df: Customer dataset
        usage_velocity: Usage velocity multiplier

    Returns:
        DataFrame with segment analysis
    """
    df_copy = df.copy()
    df_copy["churn_risk"] = calculate_churn_risk_scores(df_copy, usage_velocity=usage_velocity)

    analysis = df_copy.groupby("customer_segment").agg({
        "customer_id": "count",
        "churn_risk": "mean",
        "monthly_charges": ["sum", "mean"],
        "churn_status": "sum",
        "tenure": "mean",
        "last_login_days": "mean",
    }).round(2)

    analysis.columns = [
        "Customer Count",
        "Avg Churn Risk",
        "Total MRR",
        "Avg Monthly Charges",
        "Churned Count",
        "Avg Tenure",
        "Avg Days Since Login",
    ]

    return analysis.reset_index()


def get_churn_trend_by_tenure(df: pd.DataFrame, usage_velocity: float = 1.0) -> pd.DataFrame:
    """
    Analyze churn trends by customer tenure buckets.

    Args:
        df: Customer dataset
        usage_velocity: Usage velocity multiplier

    Returns:
        DataFrame with churn trends by tenure
    """
    df_copy = df.copy()
    df_copy["churn_risk"] = calculate_churn_risk_scores(df_copy, usage_velocity=usage_velocity)

    # Create tenure buckets
    df_copy["tenure_bucket"] = pd.cut(
        df_copy["tenure"],
        bins=[0, 6, 12, 24, 60, 120],
        labels=["0-6 Mo", "6-12 Mo", "1-2 Yr", "2-5 Yr", "5+ Yr"],
    )

    trend = df_copy.groupby("tenure_bucket", observed=True).agg({
        "customer_id": "count",
        "churn_status": ["sum", "mean"],
        "churn_risk": "mean",
        "monthly_charges": "mean",
    }).round(3)

    trend.columns = ["Count", "Churned", "Churn Rate", "Avg Risk", "Avg MRR"]
    trend["Churn Rate"] = (trend["Churn Rate"] * 100).round(1)

    return trend.reset_index()


def get_login_activity_analysis(df: pd.DataFrame, usage_velocity: float = 1.0) -> pd.DataFrame:
    """
    Analyze churn by login activity (last_login_days buckets).

    Args:
        df: Customer dataset
        usage_velocity: Usage velocity multiplier

    Returns:
        DataFrame with login activity analysis
    """
    df_copy = df.copy()
    df_copy["churn_risk"] = calculate_churn_risk_scores(df_copy, usage_velocity=usage_velocity)

    # Create login activity buckets
    df_copy["login_recency"] = pd.cut(
        df_copy["last_login_days"],
        bins=[0, 7, 30, 60, 90, 180],
        labels=["<7 Days", "7-30 Days", "30-60 Days", "60-90 Days", ">90 Days"],
    )

    analysis = df_copy.groupby("login_recency", observed=True).agg({
        "customer_id": "count",
        "churn_status": ["sum", "mean"],
        "churn_risk": "mean",
    }).round(3)

    analysis.columns = ["Count", "Churned", "Churn Rate", "Avg Risk"]
    analysis["Churn Rate"] = (analysis["Churn Rate"] * 100).round(1)

    return analysis.reset_index()


def simulate_usage_velocity_impact(
    df: pd.DataFrame,
    original_threshold: float,
    velocity_range: tuple = (0.1, 3.0),
) -> pd.DataFrame:
    """
    Simulate impact of usage velocity on churn metrics.

    Args:
        df: Customer dataset
        original_threshold: Original churn probability threshold
        velocity_range: Tuple of (min, max) velocity values

    Returns:
        DataFrame showing impact of velocity changes
    """
    velocities = np.arange(velocity_range[0], velocity_range[1] + 0.1, 0.2)
    results = []

    for velocity in velocities:
        kpis = calculate_kpis(df, original_threshold, usage_velocity=velocity)
        results.append({
            "Velocity": f"{velocity:.1f}x",
            "At-Risk Customers": kpis["at_risk_customers"],
            "At-Risk MRR": f"${kpis['at_risk_mrr']:,.0f}",
            "Avg Churn Risk": f"{kpis['avg_churn_risk']:.2f}",
        })

    return pd.DataFrame(results)
