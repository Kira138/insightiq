# ============================================================
# InsightIQ — KPI Engine
# Connects PostgreSQL to Streamlit dashboard
# ============================================================
from urllib.parse import quote_plus
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# ── DB CONNECTION ──────────────────────────────────────────
load_dotenv()
def get_connection():
    return create_engine(os.getenv("DATABASE_URL"))
# ── KPI 1: a.MONTHLY REVENUE ─────────────────────────────────
def get_monthly_revenue():
    engine = get_connection()
    query = """
        SELECT 
            TO_CHAR(o.order_purchase_timestamp, 'YYYY-MM') AS year_month,
            SUM(p.payment_value) AS total_revenue
        FROM olist_orders_dataset o
        JOIN olist_order_payments_dataset p ON o.order_id = p.order_id
        WHERE o.order_status = 'delivered'
        GROUP BY year_month
        ORDER BY year_month
    """
    return pd.read_sql(query, engine)
# ── KPI 1: b.Weekly REVENUE ─────────────────────────────────
def get_weekly_revenue():
    engine = get_connection()
    query = """
        SELECT
            DATE_TRUNC('week', o.order_purchase_timestamp) AS week,
            SUM(p.payment_value) AS total_revenue
        FROM olist_orders_dataset o
        JOIN olist_order_payments_dataset p ON o.order_id = p.order_id
        WHERE o.order_status = 'delivered'
        GROUP BY week
        ORDER BY week
    """
    return pd.read_sql(query, engine)

# ── KPI 2: ORDER VOLUME ─────────────────────────────────
def get_order_volume():
    engine=get_connection()
    query="""
       SELECT
           TO_CHAR(order_purchase_timestamp,'YYYY-MM') as year_month,count(distinct order_id) as total_orders
    FROM olist_orders_dataset 
    WHERE order_status = 'delivered'
    group by year_month
    order by year_month
    """
    return pd.read_sql(query,engine)
# ── KPI 3: AVERAGE ORDER VALUE(AOV)─────────────────────────────────
def get_AOV():
    engine=get_connection()
    query="""
       SELECT
           TO_CHAR(o.order_purchase_timestamp, 'YYYY-MM') AS year_month,
           SUM(p.payment_value) AS total_revenue,
           COUNT(DISTINCT o.order_id) AS total_orders,
           ROUND(SUM(p.payment_value)/COUNT(DISTINCT o.order_id), 2) AS aov
    FROM olist_orders_dataset o
    JOIN olist_order_payments_dataset p ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY year_month
    ORDER BY year_month
    """
    return pd.read_sql(query,engine)

# ── KPI 4a: DELIVERY SLA COMPLIANCE ─────────────────────────────────
def get_DELIVERY_SLA_COMPLIANCE():
    engine=get_connection()
    query="""
        SELECT 
    round(COUNT(*) FILTER (WHERE order_delivered_customer_date <= order_estimated_delivery_date) * 100.0 /
    COUNT(*) FILTER (WHERE order_status = 'delivered' 
                     AND order_delivered_customer_date IS NOT NULL
                     AND order_estimated_delivery_date IS NOT NULL),2) AS sla_compliance_pct
FROM olist_orders_dataset
WHERE order_status = 'delivered'
AND order_delivered_customer_date IS NOT NULL
AND order_estimated_delivery_date IS NOT NULL
     """
    return pd.read_sql(query,engine)
# ── KPI 4b: DELIVERY SLA COMPLIANCE by Month ─────────────────────────────────
def get_SLA_Compliance_byMonth():
    engine=get_connection()
    query="""
          SELECT 
              TO_CHAR(order_purchase_timestamp, 'YYYY-MM') AS year_month,
	          round(COUNT(*) FILTER (WHERE order_delivered_customer_date <= order_estimated_delivery_date) * 100.0 /
              COUNT(*) FILTER (WHERE order_status = 'delivered' 
                     AND order_delivered_customer_date IS NOT NULL
                     AND order_estimated_delivery_date IS NOT NULL),2) AS sla_compliance_pct
FROM olist_orders_dataset
WHERE order_status = 'delivered'
AND order_delivered_customer_date IS NOT NULL
AND order_estimated_delivery_date IS NOT NULL
group by year_month
order by year_month
"""
    return pd.read_sql(query,engine)

# ── KPI 5: CUSTOMER RETENSION RATE ─────────────────────────────────
def get_customer_retension_rate():
    engine=get_connection()
    query="""
         Select 
           round(
           (select count(*)*100.0
from (
      SELECT c.customer_unique_id 
FROM olist_orders_dataset o
JOIN olist_customers_dataset c
    ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_unique_id
HAVING COUNT(o.order_id) > 1) 
 as customers_who_reordered
 )
 /
 (
 Select
 count(DISTINCT c.customer_unique_id) 
 from olist_customers_dataset as c
 join olist_orders_dataset o 
     ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
 ),2) as ratio
    """
    return pd.read_sql(query,engine)
# ── KPI 6: SELLER PERFORMANCE SCORE ─────────────────────────────────
def get_seller_performance_score():
    engine=get_connection()
    query="""
            select i.seller_id,count(i.order_item_id) as total_orders,round(avg(r.review_score),1) as average_review_score,
            round(avg(date(o.order_delivered_customer_date) -date(o.order_purchase_timestamp)),1) as avg_delivery_day,
            RANK() OVER (order by avg(r.review_score) desc) as performance_rank
from olist_order_reviews_dataset as r Join olist_orders_dataset as o 
on r.order_id = o.order_id
Join olist_order_items_dataset as i 
on o.order_id=i.order_id
where o.order_status='delivered'
group by seller_id 
order by avg(r.review_score) desc
    """
    return pd.read_sql(query,engine)
# ── KPI 7: REVENUE BY REGION ─────────────────────────────────
def get_revenue_by_region():
    engine=get_connection()
    query="""
             Select sum(p.payment_value) as total_revenue, c.customer_state
from olist_order_payments_dataset as p JOIN olist_orders_dataset as o
on p.order_id=o.order_id
JOIN olist_customers_dataset as c
on o.customer_id= c.customer_id
where o.order_status='delivered'
group by c.customer_state
order by sum(p.payment_value) desc
    """
    return pd.read_sql(query,engine)
# ── KPI 8: CATEGORY WISE SALES GROWTH ─────────────────────────────────
def get_category_wise_sales_growth():
    engine=get_connection()
    query="""
    Select sum(pa.payment_value) as total_revenue,
    COALESCE(e.product_category_name_english, p.product_category_name, 'Unknown') AS category,
    To_char(o.order_purchase_timestamp, 'YYYY-MM')AS year_month
from olist_order_items_dataset as i JOIN olist_products_dataset as p
on i.product_id=p.product_id
join olist_order_payments_dataset as pa
on pa.order_id=i.order_id
join olist_orders_dataset as o
on pa.order_id=o.order_id
left join product_category_name_translation as e
on e.product_category_name=p.product_category_name
where order_status='delivered'
group by p.product_category_name,year_month,e.product_category_name_english
order by year_month asc
    """
    return pd.read_sql(query,engine)
# ── KPI 9: Customer Churn by Month ─────────────────────────────────
def get_Customer_Churn_by_Month():
    engine=get_connection()
    query="""
    Select To_char(last_purchase_date_per_customer::date,'YYYY-MM')as churn_month,count(distinct customer_unique_id) as churned_customer
from(Select distinct c.customer_unique_id,TO_CHAR(max(o.order_purchase_timestamp),'YYYY-MM-DD') as last_purchase_date_per_customer
from olist_customers_dataset as c JOIN olist_orders_dataset as o
on c.customer_id=o.customer_id
where o.order_purchase_timestamp<(select max(order_purchase_timestamp) from olist_orders_dataset)-INTERVAL '60 days'
group by c.customer_unique_id) as churned
group by churn_month
order by churn_month
 """
    return pd.read_sql(query,engine)
# ── KPI 10: cohort analysis─────────────────────────────────
def get_cohort_retention():
    engine=get_connection()
    query="""
       SELECT 
    first_order_date,
    cohort_month,
    customers,
    ROUND(customers * 100.0 / 
        FIRST_VALUE(customers) OVER (
            PARTITION BY first_order_date 
            ORDER BY cohort_month
        ), 2) AS retention_pct 
FROM (
    SELECT 
        first_order_date,
        cohort_month,
        COUNT(DISTINCT customer_unique_id) AS customers
    FROM (
        SELECT 
            first_order_month AS first_order_date,
            customer_unique_id,
            DATE_PART('year', AGE(
                order_purchase_timestamp::date, 
                (first_order_month || '-01')::date)) * 12 +
            DATE_PART('month', AGE(
                order_purchase_timestamp::date, 
                (first_order_month || '-01')::date)) AS cohort_month
        FROM (
            SELECT 
                cohort_start.first_order_month,
                cohort_start.customer_unique_id,
                o.order_purchase_timestamp
            FROM (
                SELECT c.customer_unique_id,
                    TO_CHAR(MIN(o.order_purchase_timestamp),'YYYY-MM') AS first_order_month
                FROM olist_customers_dataset c 
                JOIN olist_orders_dataset o ON c.customer_id = o.customer_id
                GROUP BY c.customer_unique_id
            ) AS cohort_start
            JOIN olist_customers_dataset c ON cohort_start.customer_unique_id = c.customer_unique_id
            JOIN olist_orders_dataset o ON c.customer_id = o.customer_id
            WHERE o.order_status = 'delivered'
        ) AS cohort_data
    ) AS cohort_details
    GROUP BY first_order_date, cohort_month
) AS cohort_counts
ORDER BY first_order_date, cohort_month
    """
    return pd.read_sql(query,engine)
# ── TEST CONNECTION ────────────────────────────────────────
if __name__ == "__main__":
    engine = get_connection()
    print("Connected to InsightIQ database!")
    df = get_monthly_revenue()
    print("\n── KPI 1: a.Monthly Revenue ──")
    print(df)
    df = get_weekly_revenue()
    print("\n── KPI 1: b.Weekly Revenue ──")
    print(df)
    df=get_order_volume()
    print("\n── KPI 2: order volume ──")
    print(df)
    df=get_AOV()
    print("\n── KPI 3: AOV ──")
    print(df)
    df=get_DELIVERY_SLA_COMPLIANCE()
    print("\n── KPI 4: SLA Compliance ──")
    print(df)
    df=get_customer_retension_rate()
    print("\n── KPI 5: Customer Retension Rate ──")
    print(df)
    df=get_seller_performance_score()
    print("\n── KPI 6: Seller Performance Score ──")
    print(df)
    df=get_revenue_by_region()
    print("\n── KPI 7: Revenue By Region ──")
    print(df)
    df=get_category_wise_sales_growth()
    print("\n── KPI 8: Category Wise Sales Growth ──")
    print(df)
    df=get_SLA_Compliance_byMonth()
    print("\n---KPI 4b: SLA Compliance by Month---")
    print(df)
    df=get_Customer_Churn_by_Month()
    print("\n── KPI 9: Customer Churn by Month ──")
    print(df)
    df=get_cohort_retention()
    print("\n── KPI 10: cohort analysis──────────")
    print(df)


    #Results Summary:

 #      KPI                                   Result
 # Monthly Revenue                      2016-10 to 2018-08
 # Order Volume                         Peak: Nov 2017 (7,289 orders)
 # AOV                                  Average ~R$160 per order
 # SLA Compliance                       91.89% — above 85% target!
 # Customer Retention                           3%
 # Seller Performance                   2,965 sellers ranked
 # Revenue by Region                    SP dominates at R$5.77M
 # Category Sales Growth                1,272 rows of monthly data

##Interesting findings!
#November 2017 = highest orders (7,289) — Black Friday! 
#SLA = 91.89% — beating the 85% target! 
#AOV dropping slightly over time — worth investigating!