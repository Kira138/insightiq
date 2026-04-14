import streamlit as st
import pandas as pd
import plotly.express as px
from kpi_engine import get_monthly_revenue
from kpi_engine import get_order_volume
from kpi_engine import get_AOV
from kpi_engine import get_SLA_Compliance_byMonth
from kpi_engine import get_category_wise_sales_growth
from kpi_engine import get_seller_performance_score
import plotly.graph_objects as go
from ai_summaries import generate_kpi_summary

# ── PAGE CONFIG ──────────────────────────────
st.set_page_config(
    page_title="InsightIQ",
    page_icon="📊",
    layout="wide"
)

# ── TITLE ────────────────────────────────────
st.title("📊 InsightIQ — Business Intelligence Dashboard")
st.markdown("AI-Powered Analytics for Olist E-Commerce")

# ── SIDEBAR ──────────────────────────────────
st.sidebar.title("Filters")
st.sidebar.markdown("---")

# Date range filter
st.sidebar.subheader("📅 Date Range")
start_date = st.sidebar.selectbox(
    "Start Month",
    options=['2016-10', '2017-01', '2017-06', '2018-01'],
    index=0
)

end_date = st.sidebar.selectbox(
    "End Month", 
    options=['2017-12', '2018-03', '2018-06', '2018-08'],
    index=3
)

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Navigation")
page = st.sidebar.radio(
    "Select KPI",
    ["Overview", "Revenue", "Orders", "Customers", "Sellers"]
)

#st.write(f"Selected: {start_date} to {end_date}")
#st.write(f"Page: {page}")
st.sidebar.markdown("---")
st.sidebar.subheader("📁 Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=['csv'])
if uploaded_file is None:
   col1, col2 , col3, col4 = st.columns(4)
   col_left, col_right = st.columns(2)

#─────────────────────Revenue KPI Card & line graph───────────────────────────
   with col1:
     df_revenue= get_monthly_revenue()
     df_filtered=df_revenue[
     (df_revenue['year_month']>=start_date) &
     (df_revenue['year_month']<=end_date)
     ]
     current=df_filtered['total_revenue'].iloc[-1]
     previous=df_filtered['total_revenue'].iloc[-2]
     delta=(current-previous)/previous*100
     st.metric(
      label="Total Revenue",
      value=f"R$ {current:,.0f}",
      delta=f"{delta:.1f}%"
     )
     fig = px.line(                
        df_filtered,        
        x='year_month', 
        y='total_revenue', 
        title='Monthly Revenue Trend',
        labels={'total_revenue': 'Revenue (R$)', 'year_month': 'Month'}
       
     )
     st.plotly_chart(fig)
     if st.button("Revenue Insight"):
        with st.spinner("Generating insight..."):
            summary = generate_kpi_summary(
                "Total Revenue",
                f"R$ {current:,.0f}",
                delta
            )
            st.info(summary)
#f"R$ {current:,.0f}" explained:
#f" " → f-string (inserts variable)
#{current:,.0f} → formats number with commas, no decimals
#Example: 985414 → R$ 985,414
#f"{delta:.1f}%" explained:
#{delta:.1f} → 1 decimal place
#Example: -4.1% or +53.6%

#df_filtered after user selects 2016-10 to 2018-08:
#Row 0:  2016-10  → 46,566
#Row 1:  2017-01  → 127,545
#...
#Row 20: 2018-07  → 1,027,903  ← iloc[-2] = PREVIOUS
#Row 21: 2018-08  → 985,414    ← iloc[-1] = CURRENT
#───────────────────── Order Volume KPI Card & line graph───────────────────────────
   with col2:
     df_order_volume= get_order_volume()
     df_filtered=df_order_volume[
     (df_order_volume['year_month']>=start_date) &
     (df_order_volume['year_month']<=end_date)
     ]
     current=df_filtered['total_orders'].iloc[-1]
     previous=df_filtered['total_orders'].iloc[-2]
     delta=(current-previous)/previous*100
     st.metric(
       label="Order Volume",
       value=f"{current:,.0f}",
       delta=f"{delta:.1f}%"
     )
     fig = px.line(                
        df_filtered,        
        x='year_month', 
        y='total_orders', 
        title='Monthly Order Trend',
        labels={'total_orders': 'Orders', 'year_month': 'Month'}
     )
     st.plotly_chart(fig)
     if st.button("Order Volume Insight"):
        with st.spinner("Generating insight..."):
            summary = generate_kpi_summary(
                "Order Volume",
                f"{current:,.0f} orders",
                delta
            )
            st.info(summary)
#───────────────────── AOV KPI Card & line graph───────────────────────────
   with col3:
     df_AOV= get_AOV()
     df_filtered=df_AOV[
     (df_AOV['year_month']>=start_date) &
     (df_AOV['year_month']<=end_date)
     ]
     current=df_filtered['aov'].iloc[-1]
     previous=df_filtered['aov'].iloc[-2]
     delta=(current-previous)/previous*100
     st.metric(
       label="AOV",
       value=f"{current:,.0f}",
       delta=f"{delta:.1f}%"
     )
     fig = px.line(                
        df_filtered,        
        x='year_month', 
        y='aov', 
        title='AOV Trend',
        labels={'aov': 'AOV', 'year_month': 'Month'}
     )
     st.plotly_chart(fig)
     if st.button("AOV Insight"):
        with st.spinner("Generating insight..."):
            summary = generate_kpi_summary(
                "AOV",
                f" {current:,.0f}",
                delta
            )
            st.info(summary)
#───────────────────── SLA_Compliance KPI Card & line graph───────────────────────────
   with col4:
     df_SLA= get_SLA_Compliance_byMonth()
     df_filtered=df_SLA[
     (df_SLA['year_month']>=start_date) &
     (df_SLA['year_month']<=end_date)
     ]
     current=df_filtered['sla_compliance_pct'].iloc[-1]
     previous=df_filtered['sla_compliance_pct'].iloc[-2]
     delta=(current-previous)/previous*100
     st.metric(
       label="SLA Compliance",
       value=f"{current:,.1f}%",
       delta=f"{delta:.1f}%"
     )
     fig = px.line(                
        df_filtered,        
        x='year_month', 
        y='sla_compliance_pct', 
        title='SLA Compliance Trend',
        labels={'sla_compliance_pct': 'SLA%', 'year_month': 'Month'}
    )
     st.plotly_chart(fig)
     if st.button("SLA Compliance Insight"):
        with st.spinner("Generating insight..."):
            summary = generate_kpi_summary(
                "SLA Compliance",
                f"{current:,.1f}",
                delta
            )
            st.info(summary)
     st.markdown("---")  # divider line

   if st.button("📊 Generate Full Report"):
     with st.spinner("Generating full report..."):
        st.subheader("📋 Executive Summary Report")
        
        # Revenue summary
        df_rev = get_monthly_revenue()
        df_f = df_rev[(df_rev['year_month']>=start_date) & (df_rev['year_month']<=end_date)]
        current = df_f['total_revenue'].iloc[-1]
        previous = df_f['total_revenue'].iloc[-2]
        delta = (current-previous)/previous*100
        st.write("**Revenue:**")
        st.info(generate_kpi_summary("Total Revenue", f"R$ {current:,.0f}", delta))
        
        # Orders summary
        df_order_volume= get_order_volume()
        df_filtered=df_order_volume[
        (df_order_volume['year_month']>=start_date) &
        (df_order_volume['year_month']<=end_date)
        ]
        current=df_filtered['total_orders'].iloc[-1]
        previous=df_filtered['total_orders'].iloc[-2]
        delta=(current-previous)/previous*100
        st.write("**Order Volume:**")
        st.info(generate_kpi_summary("Order Volume", f" {current:,.0f} order", delta))

        # AOV summary
        df_AOV= get_AOV()
        df_filtered=df_AOV[
        (df_AOV['year_month']>=start_date) &
        (df_AOV['year_month']<=end_date)
        ]
        current=df_filtered['aov'].iloc[-1]
        previous=df_filtered['aov'].iloc[-2]
        delta=(current-previous)/previous*100
        st.write("**AOV:**")
        st.info(generate_kpi_summary("AOV", f"{current:,.0f}", delta))

        # SLA summary
        df_SLA= get_SLA_Compliance_byMonth()
        df_filtered=df_SLA[
        (df_SLA['year_month']>=start_date) &
        (df_SLA['year_month']<=end_date)
        ]
        current=df_filtered['sla_compliance_pct'].iloc[-1]
        previous=df_filtered['sla_compliance_pct'].iloc[-2]
        delta=(current-previous)/previous*100
        st.write("**SLA Compliance:**")
        st.info(generate_kpi_summary("SLA Compliance", f"{current:,.1f}", delta))
        # your generate_kpi_summary call here
#───────────────────── Category wise revenue & treemap───────────────────────────
     with col_left:
        df_category=get_category_wise_sales_growth()
        df_filtered=df_category[
        (df_category['year_month']>=start_date) &
        (df_category['year_month']<=end_date)
        ]
        result=df_filtered.groupby('category')['total_revenue'].sum().reset_index()
        fig=px.treemap(
            result,
            path=['category'],
            values='total_revenue',
            title='Revenue by Category'
        )
        st.plotly_chart(fig)

     with col_right:
       pass # empty for now — add chart later!

#─────────────────────Seller leaderboard table with sort/filter────────────────
     df_seller_leaderboard=get_seller_performance_score()
     seller_leaderboard=df_seller_leaderboard.sort_values(by='average_review_score',ascending=False)
     fig=go.Figure(data=[go.Table(
        header=dict(
        values=list(seller_leaderboard.columns),
        fill_color='black',
        font=dict(color='white', size=16),
        align='center'
        ),
      cells=dict(
        values=[seller_leaderboard[col] for col in seller_leaderboard.columns],
        fill_color=['#1a1a2e', '#16213e'],
        align='center'
      )
  )])

     fig.update_layout(title='Leaderboard')
#fig.show()
     st.plotly_chart(fig)
#-------------------------CSV File---------------------------------------
else:
  st.sidebar.markdown("---")
  st.sidebar.subheader("Upload Your Data")
  

  if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    if len(df.columns) < 2:      # ← check columns FIRST!
      st.error("File needs at least 2 columns!")
      st.stop()
    elif df.empty:                # ← then check empty
      st.error("Uploaded file is empty!")
    else: 
      st.success(f"File uploaded! {len(df)} rows, {len(df.columns)} columns")
      # Show preview
      st.subheader("📋 Data Preview")
      st.dataframe(df.head())
      # Column selectors
      date_col = st.selectbox(
      "Select date column", 
      ["-- Select --"] + list(df.columns)
      )
      value_col = st.selectbox("Select value column", ["-- Select --"] + list(df.columns))
# ----------------After column selectors--------------------------------------
    if date_col != "-- Select --" and value_col != "-- Select --":
       if date_col == value_col:
         st.warning("⚠️ Please select different columns!")
       else:
          df[date_col] = pd.to_datetime(df[date_col])
          df = df.sort_values(by=date_col)
          fig = px.line(
            df,
            x=date_col,
            y=value_col,
            title=f'{value_col} over time'
           )
          st.plotly_chart(fig)