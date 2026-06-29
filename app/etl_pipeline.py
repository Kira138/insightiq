import boto3
import pandas as pd
import os
from dotenv import load_dotenv
from io import StringIO
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy import text 

load_dotenv()

# Connect to S3
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

def read_csv_from_s3(filename):
    bucket = os.getenv('AWS_BUCKET_NAME')
    obj = s3.get_object(Bucket=bucket, Key=filename)
    df = pd.read_csv(obj['Body'])
    print(f"Loaded {filename}: {len(df)} rows")
    return df

def extract_all_from_s3():
    files = [
        'olist_orders_dataset.csv',
        'olist_customers_dataset.csv',
        'olist_order_items_dataset.csv',
        'olist_order_payments_dataset.csv',
        'olist_order_reviews_dataset.csv',
        'olist_products_dataset.csv',
        'olist_sellers_dataset.csv',
        'olist_geolocation_dataset.csv',
        'product_category_name_translation.csv'
    ]
    dataframes = {}
    for file in files:
        name = file.replace('.csv', '')
        dataframes[name] = read_csv_from_s3(file)
    return dataframes

def transform_orders(df):
    date_cols = [
        'order_purchase_timestamp',
        'order_approved_at',
        'order_delivered_carrier_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col])
    df = df.dropna(subset=['order_id', 'customer_id'])
    print(f" Transformed orders: {len(df)} rows")
    return df

def transform_customers(df):
    df = df.dropna(subset=['customer_id', 'customer_unique_id'])
    print(f" Transformed customers: {len(df)} rows")
    return df

def transform_products(df):
    df['product_category_name'] = df['product_category_name'].fillna('unknown')
    df = df.dropna(subset=['product_id'])
    print(f" Transformed products: {len(df)} rows")
    return df

def transform_order_items(df):
    df = df.dropna(subset=['order_id', 'product_id'])
    print(f" Transformed order_items: {len(df)} rows")
    return df

def get_db_engine():
    db_url = os.getenv('DATABASE_URL')
    engine = create_engine(db_url)
    return engine

def load_to_postgres(df, table_name, engine):
    df.to_sql(
        table_name,
        engine,
        if_exists='replace',
        index=False
    )
    print(f" Loaded {table_name}: {len(df)} rows")

def create_star_schema(engine):
    with engine.connect() as conn:
         # Customer Dimension
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_customer AS
            SELECT 
                customer_id,
                customer_unique_id,
                customer_state
            FROM olist_customers_dataset
        """))
        
        print(" dim_customer created!")
             # Product Dimension
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_product AS
            SELECT 
                product_id,
                product_category_name
            FROM olist_products_dataset
        """))
        print(" dim_product created!")
             #Seller Dimension
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_seller AS
            SELECT 
                seller_id,
                seller_state
            FROM olist_sellers_dataset
        """))
        print(" dim_seller created!")
              #Order Dimension
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_order AS
            SELECT 
                order_id,
                order_status,
                order_delivered_carrier_date,
                order_delivered_customer_date,
                order_estimated_delivery_date
            FROM olist_orders_dataset
        """))
        print(" dim_order created!")
              #Date Dimension
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_date  (
                date_id INT PRIMARY KEY,
                full_date DATE,
                year INT,
                month INT,
                quarter INT,
                day_of_week VARCHAR(20)
            );
        """))
        print(" dim_date created!")
        # Fact Table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS fact_order_items AS
            SELECT 
               oi.order_id,
               o.customer_id,
               oi.product_id,
               oi.seller_id,
               o.order_purchase_timestamp::date AS order_date,
               oi.price,
               oi.freight_value
            FROM olist_order_items_dataset oi
            JOIN olist_orders_dataset o ON oi.order_id = o.order_id
        """))
        print(" fact_order_items created!")
        conn.commit()

if __name__ == "__main__":
    print("Starting ETL pipeline...")
    dataframes = extract_all_from_s3()
    
    # Transform
    dataframes['olist_orders_dataset'] = transform_orders(dataframes['olist_orders_dataset'])
    dataframes['olist_customers_dataset'] = transform_customers(dataframes['olist_customers_dataset'])
    dataframes['olist_products_dataset'] = transform_products(dataframes['olist_products_dataset'])
    dataframes['olist_order_items_dataset'] = transform_order_items(dataframes['olist_order_items_dataset'])
    print("\n Transform complete!")
    
    # Load ALL 9 tables
    print("\nStarting Load step...")
    engine = get_db_engine()
    for name, df in dataframes.items():
        load_to_postgres(df, name, engine)
    print("\n ETL Pipeline Complete!")
    
    # Create Star Schema
    print("\nCreating Star Schema...")
    create_star_schema(engine)