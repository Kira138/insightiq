# InsightIQ — AI-Powered Business Intelligence Platform

## Live Demo: 
   [Click here to view InsightIQ live](https://insightiq-yswv.onrender.com)
## About: 
   InsightIQ is an end-to-end data analytics platform where users upload any business dataset and receive automated KPI dashboards, trend analysis, anomaly detection, and AI-generated executive summaries. It demonstrates the full stack of skills expected from a Data Analyst or PM: problem framing, data engineering, analytics, product thinking, and communication.
## Features: 
    1.Monthly Revenue
    2.Order Volume
    3.Average Order Value (AOV)
    4.Customer Retention Rate
    5.Seller Performance Score
    6.Delivery SLA Compliance
    7.Product Category Revenue Share
    8.Churn Signal
    9.Analytics — Trend Detection & Forecasting   
    10.Streamlit Dashboard 
    11.AI Executive Summaries
    12.User can get their own predictions fo their dataset
    13.PDF Download for the reports
## Dataset:
    Used the publicly available Brazilian E-Commerce dataset (Olist) from Kaggle — 100K+ real orders with seller data, product info, payment details, reviews, and geolocation.
## Tech Stack: 
   1.PostgreSQL-Industry standard SQL — on every DA job spec
   2.Python (pandas, numpy)-Core DA toolkit; fast and widely used
   3.Prophet, scikit-learn, statsmodels-Time-series forecasting + anomaly detection
   4.Plotly-Interactive charts for the dashboard
   5.Streamlit-Fast to build, looks professional, Python-native
   6.Claude API-Auto-generate executive summaries per KPI
   7.Render.com (free tier)-Live URL to share with recruiters
   8.GitHub-Portfolio-ready repo with clean README
   9.Neon-Postgres cloud
## Screenshots
    ### Default Screen
    ![Default Screen](docs/screenshots/01_default.png)
    ### Dashboard with KPI Cards
    ![Dashboard](docs/screenshots/02_dashboard.png)
    ### Treemap & KPI Warnings
    ![Treemap](docs/screenshots/03_treemap_warnings.png)
    ### Executive Report & PDF
    ![Report](docs/screenshots/04_report_pdf.png)
    ### Seller Leaderboard
    ![Leaderboard](docs/screenshots/05_leaderboard.png)
## How to Run Locally
   1.Clone the repo
   git clone https://github.com/Kira138/insightiq.git
   cd insightiq
   2.Install dependencies
   pip install -r requirements.txt
   3.Create a .env file
   ANTHROPIC_API_KEY=your_claude_api_key_here
   DATABASE_URL=your_neon_connection_string_here
   4.Run the app
   streamlit run app/main.py
## Coming Soon
   1.AWS S3 Integration
   2.Star Schema Design
   3.ETL Pipeline
   4.Tableau Public Dashboard
   5.Business Requirements Document (BRD)
