import pandas as pd
from prophet import Prophet
from app.kpi_engine import get_SLA_Compliance_byMonth

def get_SLA_drop_anomaly():
    df=get_SLA_Compliance_byMonth()
    df=df.dropna()
    anomolies=df[(df['sla_compliance_pct']<85)].copy()
    anomolies['anomoly_type']=None
    anomolies.loc[anomolies['sla_compliance_pct']<85,'anomoly_type']='Drop'
    return anomolies

if __name__=="__main__":
    print(get_SLA_drop_anomaly())

#Feb-Mar 2018 dropped below 85%