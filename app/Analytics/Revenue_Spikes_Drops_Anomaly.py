import pandas as pd
from prophet import Prophet
from app.kpi_engine import get_monthly_revenue
from app.Analytics.MoM_analytics import get_mom_change

def detect_revenue_anomalies():
  df=get_mom_change()
  df = df.dropna()  #dropna() removes those NaN rows
  #Takes df from line 8 
  #Filters only rows where mom_change_pct > 50 OR < -30
  #.copy() creates independent copy — safe to modify
  #Stores filtered rows in anomalies
  anomalies=df[(df['mom_change_pct'] > 50) | (df['mom_change_pct'] < -30)].copy() 
  #Takes anomalies from line 3
  #Adds new empty column called anomaly_type
  #All values = None for now
  anomalies['anomaly_type']=None
  #Takes anomalies from line 4
  #Finds rows where mom_change_pct > 50
  #Sets anomaly_type = 'Spike'/'Drop' for those rows
  anomalies.loc[anomalies['mom_change_pct']>50, 'anomaly_type']='Spike'
  anomalies.loc[anomalies['mom_change_pct']<-30, 'anomaly_type']='Drop'
  return anomalies
  
if __name__=="__main__":
  print (detect_revenue_anomalies())

#Black Friday +53% spike!


