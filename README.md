# Churn Insight & Intervention Portal

A professional, production-ready Streamlit application for customer churn prediction, risk assessment, and intervention management with **interactive scenario simulation**.

## 🎯 Overview

This application provides teams with:
- **Real-time Churn Prediction**: ML-based risk scoring for all customers
- **Interactive Scenario Simulation**: Three adjustable variables to model "what-if" scenarios
- **Actionable Interventions**: Data-driven recommendations prioritized by customer value
- **Professional Dashboard**: Industry-standard BI/analytics interface
- **High-Quality Synthetic Data**: Fully functional demonstration dataset (5,000 customers)

## 📁 Project Structure

```
project1/
├── app.py                    # Main Streamlit application & orchestration (16.4 KB)
├── config.py                 # All configuration, themes, constants (3.4 KB)
├── data_utils.py             # Data generation, feature engineering, analytics (15.6 KB)
├── viz_utils.py              # Professional Plotly visualizations (10.7 KB)
├── requirements.txt          # Python dependencies (4 packages)
├── README.md                 # This file
├── CLAUDE.md                 # Developer guide & architecture
├── DEPLOYMENT.md             # Multi-platform deployment guide
├── Dockerfile                # Container setup
├── docker-compose.yml        # Local development orchestration
└── .streamlit/config.toml    # Streamlit configuration
```

## 🚀 Quick Start

### Installation (< 2 minutes)

```bash
# 1. Navigate to project directory
cd C:\Sujana\project1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
streamlit run app.py

# 4. Open browser to http://localhost:8501
```

### Using Docker

```bash
docker-compose up
# Access at http://localhost:8501
```

## 📊 Application Features

### Data Schema (Synthetic)

The application generates a high-quality synthetic dataset with 5,000 customers:

| Column | Type | Range | Description |
|--------|------|-------|-------------|
| `customer_id` | String | CUST_000001... | Unique customer identifier |
| `churn_status` | Int | 0 or 1 | Actual churn (0=active, 1=churned) |
| `monthly_charges` | Float | $9.99 - $299.99 | Customer's monthly spend |
| `tenure` | Int | 1-120 months | How long they've been a customer |
| `support_tickets_count` | Int | 0-20+ | Support interactions |
| `last_login_days` | Int | 0-180 days | Days since last activity |
| `customer_segment` | String | Enterprise, Mid-Market, SMB, Personal | Business segment |

**Derived Features**: Total customer value, engagement score, support response time, renewal timeline

### 🎛️ Three Scenario Simulation Variables

#### 1. **Churn Probability Threshold** (Slider: 0.1 - 0.9)
- **What it does**: Adjusts which customers are flagged as "at-risk"
- **Lower value (0.1)**: More customers flagged, broader safety net
- **Higher value (0.9)**: Only highest-risk customers flagged, focused on critical accounts
- **Use case**: Balance between retention effort and resource allocation

#### 2. **Customer Segment Filter** (Multi-select)
- **Options**: Enterprise, Mid-Market, SMB, Personal
- **What it does**: Filters dashboard to show insights for selected segments only
- **Impact**: All KPIs, charts, and recommendations update in real-time
- **Use case**: Compare segment-specific churn patterns or focus on high-value segments

#### 3. **Usage Velocity Multiplier** (Slider: 0.1 - 3.0)
- **What it does**: Simulates changes in customer login frequency impact
- **Values**:
  - **0.1x - 0.5x**: Customers less active (lower engagement = higher risk)
  - **1.0x**: Normal/baseline activity level
  - **1.5x - 3.0x**: Customers more active (higher engagement = lower risk)
- **Real-time Impact**: Watch how login activity changes affect churn predictions
- **Use case**: Model impact of engagement campaigns on churn rate

### 📈 Dashboard Sections

#### 1. Business Health Dashboard (4 KPI Cards)
- **Total Customers**: Full customer base
- **At Risk**: Count and percentage above threshold
- **Total MRR**: Monthly recurring revenue baseline
- **MRR at Risk**: Revenue exposure from at-risk customers

#### 2. Churn Risk Analysis & Trends (6 Interactive Charts)
- **Risk Distribution**: Histogram of churn scores across all customers
- **Segment Comparison**: Churn metrics by business segment (Enterprise, SMB, etc.)
- **Tenure Trend**: Churn rate & risk by customer tenure (new vs. established)
- **Login Activity Impact**: How days since login affects churn (real-time with velocity)
- **MRR at Risk Breakdown**: Revenue pie chart by risk level (Low, Medium, High)
- **Recovery Potential Gauge**: Average recovery rate of recommended interventions

#### 3. At-Risk Customers & Intervention Playbook
- **Priority Matrix**: Scatter plot (Customer Value vs. Churn Risk)
  - Each dot = one at-risk customer
  - Color = priority (Critical/High/Medium/Low)
  - Tooltip shows customer details

- **Intervention Table** (Sortable & Filterable):
  - Customer ID, Segment, Monthly Charges, Churn Risk
  - Tenure, Days Since Login, Support Tickets
  - Recommended Action (Executive Outreach, Re-engagement, etc.)
  - Priority & Estimated Recovery Rate

#### 4. Usage Velocity Impact Analysis
- **What-If Table**: Shows how velocity changes impact at-risk count and MRR exposure
- **Insights**: Recommendations based on velocity simulation
- **Key**: Demonstrates value of engagement improvements

## 🔬 Churn Risk Calculation

The application calculates churn probability using a **logistic regression-inspired model**:

```
Churn Risk = f(tenure, activity, support, value, segment, velocity)
```

**Risk Factors** (configured in `config.py`):
1. **Tenure (25% weight)**: Newer customers have higher risk
2. **Last Login Days (25% weight)**: Inactive customers more likely to churn
3. **Support Activity (15% weight)**: Indicator of satisfaction issues
4. **Monthly Charges (15% weight)**: Higher-value customers stickier
5. **Segment (20% weight)**: Enterprise lower risk, Personal higher risk

**Usage Velocity Impact**:
- Adjusts login activity's influence on risk score
- 1.0x = normal weight
- >1.0x = increased login activity = reduced risk
- <1.0x = reduced login activity = increased risk

## 🎯 Use Cases

### Use Case 1: Executive Presentation
1. Set **Segment Filter** to "Enterprise"
2. Adjust **Churn Threshold** to 0.7 (focus on critical cases only)
3. Show KPIs and Priority Matrix
4. Explain MRR at risk and recovery potential

### Use Case 2: Engagement Campaign Planning
1. Set **Usage Velocity** to 2.0x (simulate high engagement)
2. Compare "At Risk" count with baseline (1.0x)
3. Show MRR impact table
4. Quantify ROI of engagement improvements

### Use Case 3: Segment Analysis
1. Filter to specific segments (e.g., "SMB")
2. View segment-specific trends
3. Compare recovery potential across segments
4. Identify segment-specific interventions

## 📊 Data Schema Customization

To use **your own data** instead of synthetic:

### Option 1: Load from CSV
```python
# In data_utils.py, replace load_synthetic_churn_data()
@st.cache_data
def load_synthetic_churn_data(n_records=5000):
    return pd.read_csv("path/to/your/data.csv")
```

### Option 2: Load from SQL Database
```python
@st.cache_data
def load_synthetic_churn_data(n_records=5000):
    import sqlalchemy
    engine = sqlalchemy.create_engine("postgresql://user:pass@host/db")
    query = "SELECT * FROM customers WHERE created_at > NOW() - INTERVAL '2 years'"
    return pd.read_sql(query, engine)
```

### Option 3: Load from BigQuery
```python
@st.cache_data
def load_synthetic_churn_data(n_records=5000):
    from google.cloud import bigquery
    client = bigquery.Client()
    return client.query("""
        SELECT customer_id, churn_status, monthly_charges, ...
        FROM `project.dataset.customers`
    """).to_dataframe()
```

**Required Columns** (ensure these exist in your data):
```
customer_id, churn_status, monthly_charges, tenure,
support_tickets_count, last_login_days, customer_segment
```

## 🔧 Configuration

All settings in `config.py`:

```python
# Change risk thresholds
CHURN_PROBABILITY_DEFAULT = 0.5
CHURN_PROBABILITY_MIN = 0.1
CHURN_PROBABILITY_MAX = 0.9

# Adjust risk factor weights
CHURN_RISK_FACTORS = {
    "tenure": 0.25,
    "last_login_days": 0.25,
    "support_tickets_count": 0.15,
    "monthly_charges": 0.15,
    "segment_risk": 0.20,
}

# Segment risk multipliers
SEGMENT_RISK_MULTIPLIERS = {
    "Enterprise": 0.6,      # Lower risk
    "Mid-Market": 0.8,
    "SMB": 1.0,             # Baseline
    "Personal": 1.3,        # Higher risk
}

# Color palette
COLORS = {
    "primary": "#0066CC",
    "secondary": "#FF6B35",
    "success": "#00A86B",
    "danger": "#DC3545",
}
```

## 🚀 Deployment

### Streamlit Cloud (Easiest)
```bash
git push origin main  # Auto-deploys
```
Then share URL: `https://your-app-name.streamlit.app`

### Docker (Production)
```bash
docker build -t churn-portal:latest .
docker run -p 8501:8501 churn-portal:latest
```

### AWS/GCP/Azure
See **DEPLOYMENT.md** for step-by-step guides for:
- AWS ECS
- Google Cloud Run
- Azure Container Instances
- Heroku
- Kubernetes

## 📈 Performance Notes

- **Load Time**: < 2 seconds (synthetic data)
- **Chart Rendering**: < 1 second per chart
- **Interactive Filters**: Real-time updates
- **Caching Strategy**: Data cached for session lifetime

For large datasets (>1M rows), consider:
- Aggregating data before loading
- Sampling for exploratory analysis
- Pre-computing risk scores in data warehouse

## 🐛 Troubleshooting

**Issue**: Charts not rendering
- Ensure Plotly installed: `pip install plotly==5.24.0`
- Check data isn't empty: `print(filtered_df.shape)`

**Issue**: Filters not working
- Ensure segments list isn't empty
- Check for null values in segment column

**Issue**: Slow performance
- Reduce dataset size for demo
- Increase cache TTL
- Use sampling for large datasets

## 📚 API Reference

### Main Functions

**Loading Data**
```python
df = load_synthetic_churn_data(n_records=5000)
```

**Filtering**
```python
filtered_df = filter_data(df, segments=["Enterprise", "Mid-Market"])
```

**Calculating KPIs**
```python
kpis = calculate_kpis(
    df,
    churn_probability_threshold=0.5,
    usage_velocity=1.0
)
```

**Getting At-Risk Customers**
```python
at_risk = get_at_risk_customers(
    df,
    churn_probability_threshold=0.5,
    usage_velocity=1.0,
    top_n=100
)
```

**Segment Analysis**
```python
segment_stats = get_segment_analysis(df, usage_velocity=1.0)
```

See `data_utils.py` for full function signatures and docstrings.

## 📞 Support

For issues, suggestions, or questions:
- Check **CLAUDE.md** for architecture & debugging
- See **DEPLOYMENT.md** for deployment help
- Review docstrings in source files

## 📄 License

Proprietary - Internal Use Only

---

**Last Updated**: June 2024  
**Version**: 2.0.0  
**Python**: 3.9+  
**Status**: Production Ready ✅
