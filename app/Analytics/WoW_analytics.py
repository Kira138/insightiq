# Get data from kpi_engine
import pandas as pd
from prophet import Prophet
from app.kpi_engine import get_weekly_revenue

#Rename columns using Prophet & Pandas
def get_forecast_weekly_revenue(periods=10):
    df=get_weekly_revenue()
    df=df.rename(columns={'week':'ds','total_revenue':'y'})
    df['ds']=pd.to_datetime(df['ds'])

    #Build Model & Forecast
    model=Prophet()
    model.fit(df) #Train the Prophet model using our historical data
    future=model.make_future_dataframe(periods=periods, freq='W') #Create empty calendar for future dates
    forecast=model.predict(future) #Can now predict
    #forecast — contains ALL predictions:
    result=forecast[[ 'ds','yhat','yhat_lower','yhat_upper']].tail(periods) #tail() = last N rows,# gives last 10 rows
    #Since `periods=10` — we want last 10 rows = **future predictions only!
    #Because `forecast` contains BOTH:
    #Past dates (already happened) ← don't need these!
    #Future dates (predictions) ← only need these!
    #tail(periods)` cuts off the past and shows only future!
    result['yhat']=result['yhat'].round(2)
    result['yhat_lower']=result['yhat_lower'].round(2)
    result['yhat_upper']=result['yhat_upper'].round(2)
    return result

def get_WOW_revenue():
    df=get_weekly_revenue()
    df['prev_week']=df['total_revenue'].shift(1)
    df['wow_pct']=round((df['total_revenue']-df['prev_week'])/df['prev_week']*100,2)
    df = df.dropna()
    df = df[df['wow_pct'].between(-100, 200)]
    return df
if __name__ == "__main__":    #Only run this code if I'm running this file directly!
    print("Weekly Revenue")
    print(get_forecast_weekly_revenue())
    print("WoW Revenue")
    print(get_WOW_revenue())



#forecast has 100 rows:
#rows 0-89  → past dates ← ignored!
#rows 90-99 → future dates ← .tail(10) picks these! 