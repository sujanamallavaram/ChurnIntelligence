# Quick Start Guide: Churn Insight & Intervention Portal

Get the dashboard running in **2 minutes**.

## Prerequisites
- Python 3.9+
- pip (or conda)

## Installation

### Step 1: Install Dependencies
```bash
cd C:\Sujana\project1
pip install -r requirements.txt
```

**Expected output**:
```
Successfully installed streamlit-1.40.1 pandas-2.2.0 numpy-1.26.4 plotly-5.24.0
```

### Step 2: Run the Application
```bash
streamlit run app.py
```

**Expected output**:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
```

### Step 3: Open in Browser
Navigate to `http://localhost:8501` and you'll see:
- 🎛️ Sidebar with three simulation controls
- 📈 Four KPI cards showing business health
- 📊 Six interactive charts
- 🎯 At-risk customer table with recommendations

## Demo Walkthrough (5 minutes)

### 1. Explore the Baseline (1 min)
1. Open the dashboard (default values shown)
2. Look at the KPI cards: How many customers are at risk? What's the MRR exposure?
3. Note the "Churn Probability Threshold" is set to **0.5** (50%)

### 2. Adjust Churn Threshold (1 min)
1. In the sidebar, find **"Churn Probability Threshold"** slider
2. Move to **0.3** (more customers flagged as at-risk)
   - ✅ Watch KPIs update in real-time
   - ✅ See more customers appear in the table
3. Move to **0.8** (only critical cases)
   - ✅ Fewer customers, higher MRR focus

**Key Insight**: Lower threshold = wider net, higher threshold = focused on critical accounts

### 3. Filter by Segment (1 min)
1. Find **"Customer Segment Filter"** in sidebar
2. Uncheck "Personal" → See how Enterprise/SMB/Mid-Market patterns differ
3. Select only "Enterprise" → See high-value customer focus
4. Select all again to reset

**Key Insight**: Different segments have different churn patterns and intervention needs

### 4. Simulate Usage Velocity (1 min)
1. Find **"Usage Velocity Multiplier"** (default 1.0x)
2. Increase to **2.0x** (simulate high login activity)
   - 📉 Watch "At Risk" count decrease
   - 📈 Notice recovery potential improves
3. Decrease to **0.5x** (less active customers)
   - 📈 Watch churn risk spike
4. Return to **1.0x** (baseline)

**Key Insight**: Login activity is a major driver of churn. Improving engagement reduces risk.

### 5. Review Recommendations (1 min)
1. Scroll down to **"At-Risk Customers & Intervention Playbook"**
2. Examine the **Priority Matrix** (scatter plot):
   - Larger bubbles = higher value customers
   - Red = Critical, Orange = High, Blue = Medium
3. Scan the **recommendation table**:
   - What's the most common intervention? (e.g., "Re-engagement Campaign")
   - Which segments have the most critical cases?

**Key Insight**: Prioritize high-value customers first; tailor interventions by segment.

## Architecture Overview

```
User Input (Sidebar)
    ↓
Three Simulation Variables:
  1. Churn Probability (0.1-0.9)
  2. Segment Filter (multi-select)
  3. Usage Velocity (0.1-3.0x)
    ↓
Churn Risk Calculation
  (tenure, activity, support, value, segment)
    ↓
Real-time Analytics:
  - KPIs, Charts, Tables
  - All update instantly
```

## Data Schema

The application generates **5,000 synthetic customers** with:
- **customer_id**: Unique identifier
- **churn_status**: 0=active, 1=churned
- **monthly_charges**: $9.99 - $299.99
- **tenure**: 1-120 months
- **support_tickets_count**: 0-20+
- **last_login_days**: 0-180 days
- **customer_segment**: Enterprise, Mid-Market, SMB, or Personal

All data is realistic and statistically sound.

## Using Your Own Data

**To replace synthetic data with real data:**

1. Open `data_utils.py`
2. Find the `load_synthetic_churn_data()` function
3. Replace with your data loading logic:

```python
@st.cache_data
def load_synthetic_churn_data(n_records=5000):
    # Replace this with your data source
    return pd.read_csv("your_data.csv")
    # or: pd.read_sql(query, engine)
    # or: client.query(sql).to_dataframe()
```

**Ensure your data has these columns:**
```
customer_id, churn_status, monthly_charges, tenure,
support_tickets_count, last_login_days, customer_segment
```

## Common Tasks

### Change Color Scheme
Edit `config.py`:
```python
COLORS = {
    "primary": "#0066CC",      # Change to your brand color
    "danger": "#DC3545",
    ...
}
```

### Adjust Risk Thresholds
Edit `config.py`:
```python
CHURN_PROBABILITY_DEFAULT = 0.5   # Change default threshold
CHURN_PROBABILITY_MIN = 0.1       # Change min/max range
CHURN_PROBABILITY_MAX = 0.9
```

### Add Customer Segments
Edit `config.py`:
```python
CUSTOMER_SEGMENTS = [
    "Enterprise",
    "Mid-Market",
    "SMB",
    "Personal",
    # Add new ones here
]
```

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install -r requirements.txt
```

### Port 8501 already in use
```bash
streamlit run app.py --server.port 8502
# Or kill existing process: lsof -i :8501
```

### Data not loading
1. Check file path in `data_utils.py`
2. Ensure required columns exist
3. Run: `python -c "import pandas as pd; df = pd.read_csv('file.csv'); print(df.columns)"`

### Filters not updating
- Ensure at least one segment is selected
- Check that data isn't empty: `print(len(filtered_df))`

## Next Steps

### For Developers
- See `CLAUDE.md` for architecture & customization
- See `DEPLOYMENT.md` for production deployment
- Review docstrings in each module

### For Business Users
- Export table data (click ⋯ on table)
- Screenshot KPIs for presentations
- Use Priority Matrix for intervention planning

### For DevOps
- See `DEPLOYMENT.md` for Docker, AWS, GCP, Azure, Heroku
- Use `docker-compose up` for local dev

## Need Help?

1. **Application Issues**: Check `data_utils.py` docstrings
2. **Customization**: See `config.py` for all settings
3. **Deployment**: Read `DEPLOYMENT.md`
4. **Architecture**: Consult `CLAUDE.md`

---

**Ready to explore?** Run `streamlit run app.py` and start investigating! 🚀
