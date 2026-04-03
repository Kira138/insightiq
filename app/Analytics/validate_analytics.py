from app.Analytics.MoM_analytics import get_mom_change
from app.Analytics.WoW_analytics import get_WOW_revenue
from app.Analytics.Revenue_Spikes_Drops_Anomaly import detect_revenue_anomalies
from app.Analytics.SLA_Drop_anomaly import get_SLA_drop_anomaly
from app.Analytics.Churn_Uptick import get_customer_Upstick_anomaly
from app.Analytics.Order_volume import get_order_volume_forecast

if __name__ == "__main__":
    print("✅ MoM Change:", get_mom_change().shape)
    print("✅ WoW Revenue:", get_WOW_revenue().shape)
    print("✅ Revenue Anomalies:", detect_revenue_anomalies().shape)
    print("✅ SLA Anomalies:", get_SLA_drop_anomaly().shape)
    print("✅ Churn Anomalies:", get_customer_Upstick_anomaly().shape)
    print("✅ Order Forecast:", get_order_volume_forecast().shape)
    print("\n All analytics functions validated!")