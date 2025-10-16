"""Sensor telemetry publisher (demo-mode).
Writes JSON lines to sim_input.jsonl to simulate Pub/Sub messages.
Each message is a sensor sample with temperature, vibration, pressure, and device metadata.
"""

import json
import random
import time
import os

OUTFILE = 'sim_input.jsonl'
SENSORS = ['motor_01','motor_02','pump_12','compressor_7']

def sample(sensor_id):
    return {
        'device_id': sensor_id,
        'ts': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'temperature': round(random.uniform(20.0, 120.0), 2),
        'vibration': round(random.uniform(0.01, 4.5), 3),
        'pressure': round(random.uniform(0.5, 12.0), 2)
    }

def append(ev):
    with open(OUTFILE,'a', encoding='utf-8') as f:
        f.write(json.dumps(ev) + '\n')

if __name__ == '__main__':
    if os.path.exists(OUTFILE):
        os.remove(OUTFILE)
    print('Starting sensor simulator — writing to', OUTFILE)
    try:
        while True:
            ev = sample(random.choice(SENSORS))
            append(ev)
            print('Wrote', ev)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print('Stopped')
