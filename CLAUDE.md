# Churn Insight & Intervention Portal - Developer Guide

## 🎯 Project Overview

**Status**: Production-ready v1.0.0  
**Platform**: Streamlit web application  
**Purpose**: Real-time customer churn risk analysis, prediction, and intervention management  
**Users**: C-suite, Operations, Customer Success, Sales teams

---

## 🏗️ Architecture

### Module Responsibility Map

```
app.py                  → Page layout, orchestration, user interaction flow
├── config.py          → All configuration, themes, constants
├── data_utils.py      → Data loading, feature engineering, calculations
└── viz_utils.py       → Chart generation, visual styling

Requirements:
- streamlit (frontend framework)
- pandas (data manipulation)
- plotly (interactive charts)
- numpy (numerical computing)
```

### Data Flow

```
User Input (Sidebar)
    ↓
Filter Selection (Date, Segment, Region)
    ↓
data_utils.filter_data()
    ↓
calculate_kpis() → KPI cards rendered
    ↓
get_intervention_recommendations() → Table & charts rendered
    ↓
viz_utils.create_*_chart() → Plotly visuals
    ↓
Browser display
```

### Key Design Decisions

1. **Modular Functions over Classes**: Each visualization and calculation is a stateless function, improving testability and reusability
2. **Streamlit Caching**: `@st.cache_data` used for expensive operations (data loading, feature engineering)
3. **Synthetic Data**: Default dataset enables demo without external dependencies; swappable for real data
4. **Color Configuration**: Centralized in `config.py` allows theme changes without touching code
5. **No State Management Library**: Uses Streamlit's native `st.session_state` for simplicity

---

## 📊 Feature Map

### Current Features (v1.0.0)

| Feature | Location | Status |
|---------|----------|--------|
| KPI Cards (4 metrics) | `app.py:render_kpi_section()` | ✅ Complete |
| Churn Trend Chart | `viz_utils.py:create_churn_trend_chart()` | ✅ Complete |
| Risk Distribution | `viz_utils.py:create_risk_distribution_chart()` | ✅ Complete |
| Segment Analysis | `viz_utils.py:create_segment_analysis_chart()` | ✅ Complete |
| MRR Impact Chart | `viz_utils.py:create_mrr_impact_chart()` | ✅ Complete |
| Region Heatmap | `viz_utils.py:create_region_heatmap()` | ✅ Complete |
| Intervention Table | `app.py:render_intervention_section()` | ✅ Complete |
| Sidebar Filters | `app.py:render_sidebar()` | ✅ Complete |
| Scenario Simulation | Threshold slider in sidebar | ✅ Complete |
| Professional Styling | CSS in `app.py` | ✅ Complete |

### Planned Features (v2.0)

- [ ] Customer drill-down detail page (customer 360)
- [ ] Historical intervention tracking (outcomes)
- [ ] ML-based churn prediction (advanced model)
- [ ] Batch intervention export (CSV/JSON)
- [ ] Email automation (notify customer success team)
- [ ] A/B testing framework (intervention effectiveness)
- [ ] Admin controls (data refresh, permissions)
- [ ] Mobile-responsive layout
- [ ] PDF report generation

---

## 🔧 Common Modifications

### Adding a New Filter

1. **Config** (`config.py`):
   ```python
   PRODUCT_TYPES = ["Enterprise", "SaaS", "Marketplace"]
   ```

2. **Data** (`data_utils.py`):
   ```python
   def filter_data(..., product_types):
       if product_types and len(product_types) < len(PRODUCT_TYPES):
           filtered_df = filtered_df[filtered_df["product_type"].isin(product_types)]
       return filtered_df
   ```

3. **Sidebar** (`app.py`):
   ```python
   selected_products = st.sidebar.multiselect(
       "Filter by product:",
       PRODUCT_TYPES,
       default=PRODUCT_TYPES
   )
   ```

4. **Main function** (`app.py`):
   ```python
   filtered_df = filter_data(..., selected_products)
   ```

### Adding a New KPI

1. **Calculation** (`data_utils.py`):
   ```python
   def calculate_kpis(df):
       return {
           "existing_kpi": value,
           "new_kpi": df["column"].mean(),  # Add here
       }
   ```

2. **Display** (`app.py`):
   ```python
   st.markdown(create_kpi_card(
       value=f"{kpis['new_kpi']:.1f}",
       label="New Metric",
       accent_color=COLORS["primary"]
   ), unsafe_allow_html=True)
   ```

### Customizing Churn Risk Formula

**Location**: `data_utils.py:calculate_churn_risk()`

Current formula uses logistic regression-inspired weighting. To adjust:
1. Modify `risk_factors` dictionary (weights)
2. Change normalization approach
3. Add/remove features
4. Test with sample data

Example: Increase weight of NPS
```python
risk_factors = {
    "nps_score": -0.25,  # Increased from -0.15
    ...
}
```

### Switching to Real Data

**Option 1: CSV File**
```python
# In data_utils.py
@st.cache_data
def load_churn_data():
    return pd.read_csv("s3://bucket/customer_data.csv")
    # Then call this instead of load_synthetic_churn_data()
```

**Option 2: SQL Database**
```python
@st.cache_data
def load_churn_data():
    import sqlalchemy
    engine = sqlalchemy.create_engine(
        "postgresql://user:pass@host:5432/db"
    )
    query = "SELECT * FROM customers WHERE account_created > NOW() - INTERVAL '2 years'"
    return pd.read_sql(query, engine)
```

**Key Requirement**: Ensure your data has these columns:
```python
required_columns = [
    "customer_id", "segment", "region", "monthly_spend",
    "churn_risk_score", "is_churned", "last_activity_date"
]
```

---

## 🐛 Debugging Tips

### Enable Debug Logging

```bash
streamlit run app.py --logger.level=debug
```

### Check Data in Sidebar

```python
# Temporary - add to render_sidebar()
with st.sidebar.expander("🐛 Debug"):
    st.write(f"Filtered rows: {len(filtered_df)}")
    st.write(f"KPIs: {kpis}")
```

### Verify Chart Data

```python
# In viz_utils.py, before returning figure
print(f"Chart data shape: {df.shape}")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
```

### Test Filters

```bash
# Run with small dataset for quick iteration
df = load_synthetic_churn_data(n_records=100)
```

---

## 📈 Performance Considerations

### Current Bottlenecks

1. **Data Loading**: Synthetic data generation is instant; real data depends on query
2. **Visualization Rendering**: 5-6 Plotly charts render in <1 second
3. **Intervention Table**: 50-100 rows display instantly

### Optimization Strategies

| Issue | Solution | Effort |
|-------|----------|--------|
| Slow data load | Add database query caching, implement pagination | Medium |
| Many users on dashboard | Scale Streamlit Cloud to Pro, use load balancer | High |
| Large intervention table | Implement server-side pagination, search filtering | Medium |
| Slow risk calculation | Pre-compute scores in data warehouse | High |

### Caching Strategy

```python
# Cache raw data (hourly refresh)
@st.cache_data(ttl=3600)
def load_data():
    return pd.read_sql(query, engine)

# Cache expensive calculations (session lifetime)
@st.cache_data
def calculate_kpis(df):
    return {...}

# Never cache user interaction (e.g., filter state)
# Use st.session_state instead
```

---

## 🧪 Testing

### Manual Testing Checklist

- [ ] All filters work independently
- [ ] Charts update when threshold changes
- [ ] Intervention table sorts correctly
- [ ] No errors in browser console
- [ ] Responsive layout on mobile (todo)
- [ ] Charts render with edge cases (empty data)

### Data Validation

```python
# Add to data_utils.py
def validate_data(df):
    assert df["customer_id"].is_unique, "Duplicate customer IDs"
    assert df["churn_risk_score"].min() >= 0 and df["churn_risk_score"].max() <= 1
    assert not df[["segment", "region"]].isnull().any()
    return True
```

### Unit Test Example

```python
# test_data_utils.py
import pytest
from data_utils import calculate_churn_risk

def test_churn_risk_range():
    df = load_synthetic_churn_data(n_records=100)
    risks = calculate_churn_risk(df)
    assert (risks >= 0).all() and (risks <= 1).all()

def test_kpi_calculation():
    df = load_synthetic_churn_data(n_records=1000)
    kpis = calculate_kpis(df)
    assert kpis["total_customers"] == 1000
    assert kpis["at_risk_customers"] <= 1000
```

---

## 🚀 Deployment Runbook

### Pre-deployment

1. Update version in this file
2. Run manual tests (see above)
3. Update DEPLOYMENT.md if needed
4. Tag git commit: `git tag v1.0.0`

### Deployment

```bash
# Streamlit Cloud (recommended)
git push origin main  # Auto-deploys

# Docker
docker build -t churn-portal:v1.0.0 .
docker push <registry>/churn-portal:v1.0.0

# Update service
kubectl set image deployment/churn-portal \
  churn-portal=<registry>/churn-portal:v1.0.0
```

### Post-deployment

1. Smoke test: Load dashboard, click filters, check charts render
2. Verify data freshness
3. Monitor error logs for first 30 minutes
4. Check user feedback channel

---

## 📞 Contacts & Resources

- **Product Owner**: [Name]
- **DevOps**: [Team/Slack]
- **Data Warehouse**: [Point of contact]
- **Design System**: See `config.py` for brand colors

---

## 📝 Changelog

### v1.0.0 (Current)
- ✅ Initial release
- ✅ 4 KPI cards
- ✅ 6 interactive charts
- ✅ Intervention recommendations table
- ✅ Sidebar scenario simulation
- ✅ Professional UI/UX

### v0.9.0 (Beta)
- Initial development
- Testing with stakeholders

---

## ⚖️ Technical Debt & Known Issues

| Issue | Impact | Priority |
|-------|--------|----------|
| No authentication | Security risk in prod | Critical |
| Synthetic data only | Can't use real metrics | High |
| No mobile responsive | Poor UX on phone | Medium |
| Limited error handling | Crashes on bad data | Medium |
| No A/B testing | Can't measure interventions | Low |

**Addressed in v2.0**: Authentication, real data integration, mobile UX

---

Last Updated: June 2024
