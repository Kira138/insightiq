import pandas as pd
from prophet import Prophet
from app.kpi_engine import get_Customer_Churn_by_Month

def get_customer_Upstick_anomaly():
    df=get_Customer_Churn_by_Month()
    df=df.dropna()
    mean=df['churned_customer'].mean()
    std_deviation=df['churned_customer'].std()
    threshold=mean+(1.2*std_deviation)
    anomolies=df[(df['churned_customer']>threshold)].copy()
    anomolies['anomaly_type'] = 'Churn_Uptick'
    return anomolies
    

if __name__=="__main__":
    df = get_Customer_Churn_by_Month()
    print("Max churn:", df['churned_customer'].max())
    print("Mean:", df['churned_customer'].mean())
    print("Std:", df['churned_customer'].std())
    print("Threshold:", df['churned_customer'].mean() + (1.5 * df['churned_customer'].std()))
    print (get_customer_Upstick_anomaly())

    #"November 2017 Black Friday brought 7,289 orders 
    #but also caused the highest churn uptick — 7,276 customers never reordered within 60 days. 
    # This reveals Olist's core challenge: high acquisition but low retention."