# InsightIQ — Case Study

## Business Problem

Business teams today are drowning in data but starving for insights. Analysts spend hours writing SQL queries, building charts, and summarizing findings manually — by the time insights reach decision makers, they're already outdated.

**The question I set out to answer:**
Can a solo developer build a fully automated BI platform that turns raw e-commerce data into actionable executive insights — in weeks, not months?

---

## My Approach

I chose the Olist Brazilian E-Commerce dataset from Kaggle — 100K+ real orders across 9 linked tables from 2016–2018. This gave me a realistic business context with enough complexity to demonstrate real analytical depth.

### The 6-Week Build:

| Week | What I Built |
|------|-------------|
| W1 | Data exploration + PostgreSQL setup |
| W2 | 8 KPI SQL queries + kpi_engine.py |
| W3 | Prophet forecasting + anomaly detection + cohort analysis |
| W4 | Streamlit dashboard + Plotly charts |
| W5 | Claude API integration + AI executive summaries |
| W6 | CSV upload + PDF export + KPI threshold alerts |
| W7 | Cloud deployment (Neon + Render.com) |

---

## Key Business Findings

### 1. Revenue Growth
Total revenue grew from R$ 46K (Oct 2016) to R$ 1.2M (Nov 2017) — a **+53% Black Friday spike** was detected as an anomaly.

### 2. Customer Retention Crisis
Customer retention rate sits at just **~3%** — far below the 20% industry benchmark. This signals a serious one-time buyer problem that needs immediate attention.

### 3. SLA Compliance Drop
Overall SLA compliance is **91.89%** — but it dropped to **78.6%** in Feb–Mar 2018, flagged automatically by the anomaly detection system.

### 4. Revenue Concentration
**São Paulo (SP) state accounts for ~26% of total revenue** — heavy geographic concentration creating business risk.

### 5. Category Insights
Top revenue categories: computers_accessories, sports_leisure, bed_bath_table — classic indicators of a tech-forward customer base.

---

##Technical Highlights

- **SQL pipelines** with complex JOINs across 9 tables
- **Prophet forecasting** for 30-day revenue + order volume predictions
- **Anomaly detection** using statistical thresholds (Z-score based)
- **Cohort analysis** for customer retention curves
- **Claude API** for auto-generating 2-sentence business summaries per KPI
- **ReportLab PDF export** for downloadable executive reports
- **Cloud deployment** on Render.com with Neon PostgreSQL

---

##What I Learned

1. **Data engineering is 80% of the work** — cleaning nulls, handling date formats, and writing reliable SQL took more time than building the UI
2. **AI APIs are powerful but fragile** — proper error handling with try/except is essential for production apps
3. **Cloud deployment reveals hidden bugs** — localhost works, but production exposes environment variable issues, port conflicts, and dependency problems
4. **Business framing matters** — a chart showing "revenue dropped 27%" means nothing without context; AI summaries bridge that gap

---

##Live Demo

[https://insightiq-yswv.onrender.com](https://insightiq-yswv.onrender.com)

**GitHub:** [https://github.com/Kira138/insightiq](https://github.com/Kira138/insightiq)

---

*Built by Kiran Jaya Prakash | Masters in Information Systems & Business Analytics | University of Illinois Springfield*


