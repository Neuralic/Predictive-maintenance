"""Simple alerter used by the pipeline. In production this would be a Cloud Function
or Cloud Run service that receives Pub/Sub notifications or HTTP webhooks.
For demo, it appends alerts to a local file and prints to stdout.
"""
import json
import requests
import time
import os

ALERT_LOG = 'output/alerts.log'
os.makedirs('output', exist_ok=True)

def send_alert(device_id, ts, prob, webhook=None):
    alert = {
        'device_id': device_id,
        'timestamp': ts,
        'failure_probability': prob
    }
    # append to local log
    with open(ALERT_LOG,'a', encoding='utf-8') as f:
        f.write(json.dumps(alert) + '\n')
    print('ALERT:', alert)
    # optional: send to a webhook (demo stub)
    if webhook:
        try:
            requests.post(webhook, json=alert, timeout=2)
        except Exception as e:
            print('Failed to send webhook (demo):', e)
    time.sleep(0.1)
