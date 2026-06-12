# 🚀 Churn Intelligence Command Center - User Guide

**Version**: 2.2.0  
**Status**: Production Ready  
**Last Updated**: June 2024

---

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard Overview](#dashboard-overview)
3. [Using Mission Control](#using-mission-control)
4. [Understanding Your Data](#understanding-your-data)
5. [Taking Action](#taking-action)
6. [Tips & Best Practices](#tips--best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Getting Started

### 🌐 Accessing the Dashboard

**Local Development:**
```
http://localhost:8501
```

**Production (Cloud):**
```
Contact your administrator for production URL
```

### ✅ System Requirements

- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection
- Screen width: 1200px+ recommended
- No special software needed

### 📱 Browser Compatibility

| Browser | Support |
|---------|---------|
| Chrome 90+ | ✅ Full |
| Firefox 88+ | ✅ Full |
| Safari 14+ | ✅ Full |
| Edge 90+ | ✅ Full |
| Mobile Browsers | ⚠️ Limited |

---

## Dashboard Overview

### 🎯 Main Sections

#### 1. **Business Pulse** (Top Section)
Four KPI cards showing your business health at a glance:

| Card | What It Shows | What To Do |
|------|---------------|-----------|
| 👥 **Total Customers** | Your entire customer base | Monitor growth month-over-month |
| 🚨 **At Risk** | Customers above churn threshold | Focus interventions here |
| 💰 **Total MRR** | Monthly recurring revenue | Track revenue health |
| ⚠️ **MRR at Risk** | Revenue from at-risk customers | Prioritize high-value saves |

**How to Read**: 
- Hover over any card to see more details
- Green/normal deltas = positive trend
- Orange/inverse deltas = needs attention

---

#### 2. **Analytics Deep Dive** (Middle Section)
Six interactive charts showing detailed churn patterns:

##### 📊 **Churn Risk Distribution**
- Shows how customers spread across risk levels
- Red bars = High risk customers
- Green bars = Low risk customers
- **Use it to**: Understand overall risk profile

##### 👥 **Segment Performance**
- Compares churn across business segments
- Blue bars = Customer count per segment
- Orange bars = Average churn risk
- **Use it to**: Identify high-risk segments

##### 📅 **Tenure Impact**
- Shows how customer age affects churn
- Red bars = Churn rate by tenure
- Blue line = Average risk score
- **Use it to**: Focus on risky customer groups

##### 📵 **Login Activity Impact**
- Days since last login vs. churn rate
- Shows inactivity danger
- **Use it to**: Identify disengaged customers

##### 💎 **MRR at Risk Breakdown**
- Pie chart of revenue by risk level
- Red slice = High-risk revenue
- **Use it to**: Focus on dollar impact

##### 🎯 **Recovery Potential**
- Gauge showing intervention success likelihood
- **Use it to**: Understand recovery odds

---

#### 3. **Intervention Playbook** (Lower Section)
Actionable recommendations for each at-risk customer:

- **Priority Matrix**: Scatter plot showing which customers to prioritize
  - Left side = Lower MRR
  - Right side = Higher MRR (prioritize these!)
  - Higher up = Higher risk
  
- **Recommendations Table**:
  - Customer ID: Unique identifier
  - Segment: Business segment (Enterprise, SMB, etc.)
  - MRR: Monthly value to your business
  - Risk: Churn probability (higher = more at risk)
  - Action: What to do (call, offer discount, training, etc.)
  - Priority: Critical/High/Medium/Low
  - Recovery %: Success rate if you intervene

---

#### 4. **Velocity Impact Simulator** (Bottom Section)
See how engagement changes affect churn:

- **Low Activity (0.5x)**: Customers getting less active
- **Normal (1.0x)**: Current state
- **High Activity (2.5x)**: Customers more engaged

**Use it to**: Project impact of engagement campaigns

---

## Using Mission Control

### 🎮 The Three Control Levers

**Mission Control (left sidebar)** gives you three ways to adjust the dashboard:

---

### 1️⃣ **📊 Churn Threshold** (Blue Control Box)

**What it does**: Sets which customers are flagged as "at-risk"

**The Scale**:
- **0.10** (Far Left): Catches everyone who might churn
  - ✅ Very safe, no one slips through
  - ❌ Lots of false positives
  - 💡 Use when: You have resources to handle many leads

- **0.40** (Lower Left): Moderate sensitivity
  - Good balance of accuracy vs. coverage

- **0.50** (Middle): Default balanced setting
  - ✅ Balanced approach
  - 💡 Best for most teams

- **0.70** (Upper Right): Focused approach
  - Only high-confidence at-risk customers
  - ✅ Higher accuracy
  - ❌ Might miss some churners

- **0.90** (Far Right): Extreme focus
  - Only the riskiest customers
  - ✅ Minimal false positives
  - ❌ Misses early-warning churners

**How to Use**:
1. Move slider left/right
2. Watch KPI cards update instantly
3. Notice how "At Risk" count changes
4. Find the sweet spot for your team's capacity

**Pro Tip**: Start at 0.5, then adjust based on your team size:
- Small team (1-2 people) → 0.7-0.8
- Medium team (3-5 people) → 0.5-0.6
- Large team (5+ people) → 0.3-0.4

---

### 2️⃣ **👥 Segment Focus** (Orange Control Box)

**What it does**: Filters dashboard to show only selected customer segments

**The Segments**:
- **Enterprise**: Large accounts, high value
- **Mid-Market**: Medium-sized accounts
- **SMB**: Small/medium businesses
- **Personal**: Individual/starter users

**How to Use**:
1. Click the box to see all segments
2. Uncheck segments to exclude them
3. Dashboard updates immediately
4. All charts & metrics show only selected segments

**Use Cases**:
- Focus on Enterprise only (high value)
- Exclude Personal (high churn but low value)
- Compare Enterprise vs. SMB patterns
- Run separate strategies per segment

**Pro Tip**: 
- Check "Enterprise" only to see your VIP risk
- Compare two segments side-by-side by switching filters
- Track improvements by re-running reports for same segment

---

### 3️⃣ **⚡ Engagement Velocity** (Green Control Box)

**What it does**: Simulates changes in customer login activity

**The Scale** (0.1x to 3.0x):
- **0.1x-0.5x**: Customers getting less active
  - What if people log in half as much?
  - Churn risk increases
  - Red alert: Engagement is dropping

- **1.0x** (Middle): Current state
  - Your actual activity levels
  - Real current churn

- **1.5x-2.0x**: Customers more active
  - What if people login 2x more?
  - Churn risk drops
  - Green flag: Engagement is improving

- **2.5x-3.0x**: Heavy engagement
  - What if you doubled engagement?
  - Churn risk drops significantly

**How to Use**:
1. Move slider to adjust velocity
2. Watch "At Risk" count change
3. See how churn risk drops with engagement
4. Use this to plan engagement campaigns

**Real-World Example**:
- Current at-risk: 456 customers
- Set velocity to 2.0x (double engagement)
- New at-risk: Maybe 200 customers
- **Insight**: Doubling engagement saves ~250 customers!

**Pro Tip**: Use this to pitch engagement programs to leadership:
- "If we improve engagement, we save $XXX in MRR"
- Show the before/after metrics
- Justify investment in engagement tools

---

## Understanding Your Data

### 📊 The Metrics Explained

#### Churn Risk Score (0-100%)
**What it is**: Probability a customer will churn (cancel service)

**How it's calculated**:
- ✅ Account tenure (newer = higher risk)
- ✅ Login activity (inactive = higher risk)
- ✅ Support tickets (could indicate problems)
- ✅ Customer value (higher spend = lower risk)
- ✅ Business segment (some segments churn more)

**What to do**:
- 0-30%: Healthy customers, monitor only
- 30-60%: Watch closely, prepare interventions
- 60-90%: High risk, take action soon
- 90%+: Critical, immediate action needed

---

#### Customer Segments
**Enterprise**: Large companies, $1000+/month, strategic accounts
- Churn impact: **Critical** (high MRR loss)
- Strategy: Executive relationship, dedicated support

**Mid-Market**: Growing companies, $500-1000/month
- Churn impact: **High** (significant MRR)
- Strategy: Account management, regular check-ins

**SMB**: Small businesses, $100-500/month
- Churn impact: **Medium** (volume matters)
- Strategy: Self-service resources, community

**Personal**: Individual users, $10-100/month
- Churn impact: **Low** (small MRR each)
- Strategy: Automated nurture, low touch

---

### 🎯 Intervention Types

| Action | Best For | Success Rate |
|--------|----------|--------------|
| **Executive Outreach** | Enterprise at high risk | 70-80% |
| **Re-engagement Campaign** | Inactive customers | 50-60% |
| **Support Enhancement** | Customers with issues | 60-70% |
| **Onboarding Follow-up** | New customers | 40-50% |
| **Retention Offer** | General at-risk | 55-65% |

---

## Taking Action

### 🎯 Step-by-Step: How to Use Recommendations

#### **Step 1**: Look at Priority Matrix
- Red dots = Critical (top right)
- Orange dots = High (top middle)
- Focus on customers in top-right quadrant
- These are high-value + high-risk

#### **Step 2**: Read the Recommendation Table
- Scan the "Priority" column
- Start with "Critical" customers
- Review the "Action" column
- Note the "Recovery %" (likelihood of success)

#### **Step 3**: Take Action
```
Critical Priority:
→ Call customer directly
→ Offer executive support
→ Schedule 1-on-1 meeting
→ Provide special discount
→ Assign dedicated account manager

High Priority:
→ Send personalized email
→ Offer relevant training
→ Schedule check-in call
→ Provide limited-time offer

Medium Priority:
→ Segment email campaign
→ Webinar invitation
→ Educational content
→ Standard retention offer

Low Priority:
→ Monitor in system
→ Add to nurture campaign
→ Track behavior changes
```

#### **Step 4**: Track Results
- Update customer status after action
- Note the outcome
- Measure recovery rate
- Learn what works

---

## Tips & Best Practices

### ✅ Best Practices

1. **Check Daily**
   - Review new at-risk customers daily
   - Act within 24 hours of risk detection
   - Speed matters in retention

2. **Prioritize by Value**
   - Focus on Enterprise customers first
   - Sort by MRR in the table
   - Save $1000 MRR = save 10x $100 MRR

3. **Use Segment Filters**
   - Run separate strategies per segment
   - Enterprise needs executive touch
   - Personal needs automation
   - SMB needs account manager

4. **Test Interventions**
   - Try different actions for similar customers
   - Track what works best
   - Share learnings with team
   - Improve over time

5. **Communicate with Team**
   - Share at-risk customers with support
   - Assign interventions clearly
   - Track who's responsible
   - Follow up on outcomes

---

### 📈 Performance Tracking

**Weekly Metrics to Monitor**:
- Total at-risk customers (trending up/down?)
- MRR at risk (dollar impact)
- Intervention success rate
- Average time to intervention
- Recovery rate by segment

**Monthly Reviews**:
- Which interventions worked best?
- Which segments improved most?
- What's the ROI of interventions?
- Should we adjust our approach?

---

## Troubleshooting

### ❓ Common Questions

**Q: Why did a customer's risk suddenly increase?**
A: Check last_login_days. If they haven't logged in recently, risk goes up. Inactivity = churn risk.

**Q: Why is my MRR at Risk so high?**
A: Look at the Segment Performance chart. Are Enterprise customers showing high risk? They drive revenue.

**Q: Should I contact every at-risk customer?**
A: No. Use the Priority Matrix. Focus on top-right (high value + high risk). Skip bottom-left (low value + low risk).

**Q: How often should I check the dashboard?**
A: Daily is ideal for high-risk. Weekly minimum for overall trends.

**Q: What if a customer isn't responding to interventions?**
A: Check their engagement score. If very low, they might be ready to churn. Escalate or accept loss.

---

### 🆘 Issues & Solutions

| Issue | Solution |
|-------|----------|
| Dashboard loading slowly | Refresh page, check internet connection |
| Numbers look wrong | Check if you've filtered by segment |
| Slider not responsive | Click and drag slider, not the input box |
| Chart not showing data | Ensure at least one segment is selected |
| Can't see all recommendations | Scroll down in the table or sort by priority |

---

## 🎓 Training & Support

### For Your Team

**Onboarding Checklist**:
- [ ] Read this User Guide (15 min)
- [ ] Access dashboard (log in)
- [ ] Explore sample data (10 min)
- [ ] Try adjusting controls (5 min)
- [ ] Practice finding at-risk customers (5 min)
- [ ] Review intervention playbook (10 min)
- [ ] Do a sample intervention (15 min)

**Total Training Time**: ~1 hour

---

### Video Tutorials

Request video walkthroughs from:
- Dashboard overview (5 min)
- Using controls (5 min)
- Taking action (7 min)
- Advanced analysis (10 min)

---

### Support Contacts

- **Technical Issues**: Contact your admin
- **Data Questions**: Contact your data team
- **Strategy Questions**: Contact your retention lead
- **Feature Requests**: Submit via feedback form

---

## 📞 Getting Help

**I found a bug**: Report to technical team with screenshot
**Data looks wrong**: Check if filters are applied
**Feature request**: Email product team with use case
**Training needed**: Schedule onboarding session

---

## 📚 Additional Resources

- **README.md**: Technical overview
- **DEPLOYMENT.md**: How to run the app
- **CLAUDE.md**: Architecture & customization

---

**Last Updated**: June 2024  
**Questions?** Contact your dashboard administrator  
**Ready to improve retention?** Start with step-by-step guide above! 🚀

