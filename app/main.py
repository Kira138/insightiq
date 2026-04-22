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
from pdf_export import generate_pdf

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
    options=['Select', '2016-10', '2017-01', '2017-06', '2018-01'],
)

end_date = st.sidebar.selectbox(
    "End Month",
    options=['Select', '2017-12', '2018-03', '2018-06', '2018-08'],
)

st.sidebar.markdown("---")
st.sidebar.subheader("Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=['csv'])

if uploaded_file is None:
    if start_date == 'Select' or end_date == 'Select':
        st.info("Please select a Start Month and End Month to view the dashboard!")
    else:
        col1, col2, col3, col4 = st.columns(4)
        col_left, col_right = st.columns(2)

        # ── Revenue KPI Card & line graph ──
        with col1:
            df_revenue = get_monthly_revenue()
            df_filtered = df_revenue[
                (df_revenue['year_month'] >= start_date) &
                (df_revenue['year_month'] <= end_date)
            ]
            rev_current = df_filtered['total_revenue'].iloc[-1]
            rev_previous = df_filtered['total_revenue'].iloc[-2]
            rev_delta = (rev_current - rev_previous) / rev_previous * 100
            st.metric(
                label="Total Revenue",
                value=f"R$ {rev_current:,.0f}",
                delta=f"{rev_delta:.1f}%"
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
                        f"R$ {rev_current:,.0f}",
                        rev_delta
                    )
                    st.info(summary)

        # ── Order Volume KPI Card & line graph ──
        with col2:
            df_order_volume = get_order_volume()
            df_filtered = df_order_volume[
                (df_order_volume['year_month'] >= start_date) &
                (df_order_volume['year_month'] <= end_date)
            ]
            ord_current = df_filtered['total_orders'].iloc[-1]
            ord_previous = df_filtered['total_orders'].iloc[-2]
            ord_delta = (ord_current - ord_previous) / ord_previous * 100
            st.metric(
                label="Order Volume",
                value=f"{ord_current:,.0f}",
                delta=f"{ord_delta:.1f}%"
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
                        f"{ord_current:,.0f} orders",
                        ord_delta
                    )
                    st.info(summary)

        # ── AOV KPI Card & line graph ──
        with col3:
            df_AOV = get_AOV()
            df_filtered = df_AOV[
                (df_AOV['year_month'] >= start_date) &
                (df_AOV['year_month'] <= end_date)
            ]
            aov_current = df_filtered['aov'].iloc[-1]
            aov_previous = df_filtered['aov'].iloc[-2]
            aov_delta = (aov_current - aov_previous) / aov_previous * 100
            st.metric(
                label="AOV",
                value=f"{aov_current:,.0f}",
                delta=f"{aov_delta:.1f}%"
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
                        f" {aov_current:,.0f}",
                        aov_delta
                    )
                    st.info(summary)

        # ── SLA Compliance KPI Card & line graph ──
        with col4:
            df_SLA = get_SLA_Compliance_byMonth()
            df_filtered = df_SLA[
                (df_SLA['year_month'] >= start_date) &
                (df_SLA['year_month'] <= end_date)
            ]
            sla_current = df_filtered['sla_compliance_pct'].iloc[-1]
            sla_previous = df_filtered['sla_compliance_pct'].iloc[-2]
            sla_delta = (sla_current - sla_previous) / sla_previous * 100
            st.metric(
                label="SLA Compliance",
                value=f"{sla_current:,.1f}%",
                delta=f"{sla_delta:.1f}%"
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
                        f"{sla_current:,.1f}",
                        sla_delta
                    )
                    st.info(summary)
            st.markdown("---")

        # ── KPI Warnings ──
        st.subheader("KPI Warnings")
        if rev_delta < -20:
            st.error(f"🔴 Revenue dropped {rev_delta:.1f}% — Critical!")
        else:
            st.success(f"🟢 Revenue is good with {rev_delta:.1f}% which is lessthan threshold -20!")
        if ord_delta < -15:
            st.warning(f"🟡 Order Volume declining with {ord_delta:.1f}%!")
        else:
            st.success(f"🟢 Order Volume is good with {ord_delta:.1f}% which is lessthan threshold -15!")
        if aov_delta < -10:
            st.error(f"🔴 AOV dropped {aov_delta:.1f}% — Critical!")
        else:
            st.success(f"🟢 AOV is good with {aov_delta:.1f}% which is less than threshold -10!")
        if sla_current < 85:
            st.warning(f"🟡 SLA Compliance at {sla_current:.1f}% — below 85% target!")
        else:
            st.success(f"🟢 SLA is good with {sla_current:.1f}% which is less than threshold 85!")

        # ── Report Generation ──
        if st.button("Generate Full Report"):
            with st.spinner("Generating full report..."):
                st.subheader("Executive Summary Report")

                df_rev = get_monthly_revenue()
                df_f = df_rev[(df_rev['year_month'] >= start_date) & (df_rev['year_month'] <= end_date)]
                rev_current = df_f['total_revenue'].iloc[-1]
                rev_previous = df_f['total_revenue'].iloc[-2]
                rev_delta = (rev_current - rev_previous) / rev_previous * 100
                st.write("**Revenue:**")
                rev_summary = generate_kpi_summary("Total Revenue", f"R$ {rev_current:,.0f}", rev_delta)
                st.info(rev_summary)

                df_order_volume = get_order_volume()
                df_filtered = df_order_volume[
                    (df_order_volume['year_month'] >= start_date) &
                    (df_order_volume['year_month'] <= end_date)
                ]
                ord_current = df_filtered['total_orders'].iloc[-1]
                ord_previous = df_filtered['total_orders'].iloc[-2]
                ord_delta = (ord_current - ord_previous) / ord_previous * 100
                st.write("**Order Volume:**")
                ord_summary = generate_kpi_summary("Order Volume", f"{ord_current:,.0f}", ord_delta)
                st.info(ord_summary)

                df_AOV = get_AOV()
                df_filtered = df_AOV[
                    (df_AOV['year_month'] >= start_date) &
                    (df_AOV['year_month'] <= end_date)
                ]
                aov_current = df_filtered['aov'].iloc[-1]
                aov_previous = df_filtered['aov'].iloc[-2]
                aov_delta = (aov_current - aov_previous) / aov_previous * 100
                st.write("**AOV:**")
                aov_summary = generate_kpi_summary("AOV", f"{aov_current:,.0f}", aov_delta)
                st.info(aov_summary)

                df_SLA = get_SLA_Compliance_byMonth()
                df_filtered = df_SLA[
                    (df_SLA['year_month'] >= start_date) &
                    (df_SLA['year_month'] <= end_date)
                ]
                sla_current = df_filtered['sla_compliance_pct'].iloc[-1]
                sla_previous = df_filtered['sla_compliance_pct'].iloc[-2]
                sla_delta = (sla_current - sla_previous) / sla_previous * 100
                st.write("**SLA Compliance:**")
                sla_summary = generate_kpi_summary("SLA", f"{sla_current:,.1f}", sla_delta)
                st.info(sla_summary)

                kpi_data = {
                    'start_date': start_date,
                    'end_date': end_date,
                    'kpis': [
                        {'name': 'Total Revenue', 'value': f"R$ {rev_current:,.0f}", 'delta': f"{rev_delta:.1f}%", 'summary': rev_summary},
                        {'name': 'Order Volume', 'value': f"R${ord_current:,.0f}", 'delta': f"{ord_delta:.1f}%", 'summary': ord_summary},
                        {'name': 'AOV', 'value': f"{aov_current:,.0f}", 'delta': f"{aov_delta:.1f}%", 'summary': aov_summary},
                        {'name': 'SLA Compliance', 'value': f"{sla_current:.1f}%", 'delta': f"{sla_delta:.1f}%", 'summary': sla_summary},
                    ]
                }
                pdf = generate_pdf(kpi_data)
            st.download_button(label="📥 Download PDF Report", data=pdf, file_name="InsightIQ_Report.pdf", mime="application/pdf")

        # ── Category wise revenue & treemap ──
        with col_left:
            df_category = get_category_wise_sales_growth()
            df_filtered = df_category[
                (df_category['year_month'] >= start_date) &
                (df_category['year_month'] <= end_date)
            ]
            result = df_filtered.groupby('category')['total_revenue'].sum().reset_index()
            fig = px.treemap(
                result,
                path=['category'],
                values='total_revenue',
                title='Revenue by Category'
            )
            st.plotly_chart(fig)

        with col_right:
            pass  # empty for now — add chart later!

        # ── Seller Leaderboard ──
        df_seller_leaderboard = get_seller_performance_score()
        seller_leaderboard = df_seller_leaderboard.sort_values(by='average_review_score', ascending=False)
        fig = go.Figure(data=[go.Table(
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
        st.plotly_chart(fig)

else:
    # ── CSV Upload Section ──
    st.sidebar.markdown("---")
    st.sidebar.subheader("Upload Your Data")

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error("Could not read file — please upload a valid CSV!")
        st.stop()

    if len(df.columns) < 2:
        st.error("File needs at least 2 columns!")
        st.stop()
    elif df.empty:
        st.error("Uploaded file is empty!")
    else:
        st.success(f"File uploaded! {len(df)} rows, {len(df.columns)} columns")
        st.subheader("Data Preview")
        st.dataframe(df.head())

        date_col = st.selectbox(
            "Select date column",
            ["-- Select --"] + list(df.columns)
        )
        value_col = st.selectbox("Select value column", ["-- Select --"] + list(df.columns))

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

                if st.button("Generate CSV Insights"):
                    with st.spinner("Generating insights..."):
                        st.write(f"**Total rows:** {len(df)}")
                        st.write(f"**Date range:** {df[date_col].min()} to {df[date_col].max()}")
                        st.write(f"**{value_col} avg:** {df[value_col].mean():,.2f}")
                        st.write(f"**{value_col} max:** {df[value_col].max():,.2f}")
                        st.write(f"**{value_col} min:** {df[value_col].min():,.2f}")
                        summary = generate_kpi_summary(
                            value_col,
                            f"{df[value_col].mean():,.2f}",
                            0
                        )
                        st.info(summary)