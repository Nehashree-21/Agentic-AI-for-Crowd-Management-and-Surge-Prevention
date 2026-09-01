from backend.database.alert_service import (
    save_alert,
    get_recent_alerts
)


save_alert(
    alert_type="SURGE",
    severity="CRITICAL",
    message="Abnormal crowd movement detected",
    confidence=0.89
)

print("Alert saved successfully!")

alerts = get_recent_alerts(5)

print("\nRecent alerts:")

for alert in alerts:
    print(alert)