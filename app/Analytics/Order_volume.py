import pandas as pd
from prophet import Prophet
from app.kpi_engine import get_order_volume

def get_order_volume_forecast(periods=10):
    df=get_order_volume()
    df=df.rename(columns={'year_month':'ds','total_orders':'y'})
    df['ds']=pd.to_datetime(df['ds'])
    df = df.dropna()
    
    model=Prophet()
    model.fit(df)
    future=model.make_future_dataframe(periods=periods,freq='ME')
    forecast=model.predict(future)
    result=forecast[['ds','yhat','yhat_lower','yhat_upper']].tail(periods)
    result['yhat']=result['yhat'].round(2)
    result['yhat_lower']=result['yhat_lower'].round(2)
    result['yhat_upper']=result['yhat_upper'].round(2)
    return result
if __name__=="__main__":
    print(get_order_volume_forecast())

#python3 -m app.Analytics.Order_volume