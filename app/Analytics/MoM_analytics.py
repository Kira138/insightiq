import pandas as pd
from prophet import Prophet
from app.kpi_engine import get_monthly_revenue

def forecast_revenue(periods=5):
    df = get_monthly_revenue()
    df = df.rename(columns={
        'year_month': 'ds',
        'total_revenue': 'y'
    })
    df['ds'] = pd.to_datetime(df['ds'])
    
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=periods, freq='MS')
    forecast = model.predict(future)
    
    result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
    result['yhat'] = result['yhat'].round(2)
    result['yhat_lower'] = result['yhat_lower'].round(2)
    result['yhat_upper'] = result['yhat_upper'].round(2)
    
    return result

def get_mom_change():
    df = get_monthly_revenue()
    df['prev_month'] = df['total_revenue'].shift(1)
    df['mom_change_pct'] = round(
        (df['total_revenue'] - df['prev_month']) / df['prev_month'] * 100, 2
    )
    return df

if __name__ == "__main__":
    print("Revenue Forecast:")
    result = forecast_revenue()
    print(result)
    
    print("\nMoM Change:")
    print(get_mom_change())