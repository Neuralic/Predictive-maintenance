"""Demo-mode Apache Beam pipeline for predictive maintenance.
Reads JSON lines from sim_input.jsonl (simulated Pub/Sub), runs feature extraction,
calls a mock predictor (vertex_model.mock_vertex_predict), writes scored records
to output/predictions.csv and triggers alerts when probability exceeds threshold.
"""
import os
import json
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from vertex_model import mock_vertex_predict
from alerter import send_alert

OUTPUT_DIR = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)
PRED_FILE = os.path.join(OUTPUT_DIR, 'predictions.csv')

class Parse(beam.DoFn):
    def process(self, line):
        if isinstance(line, bytes):
            line = line.decode('utf-8')
        try:
            yield json.loads(line)
        except:
            return

class Score(beam.DoFn):
    def process(self, row):
        features = {
            'temperature': row.get('temperature', 0.0),
            'vibration': row.get('vibration', 0.0),
            'pressure': row.get('pressure', 0.0)
        }
        prob = mock_vertex_predict(features)
        out = {
            'device_id': row.get('device_id'),
            'ts': row.get('ts'),
            'temperature': features['temperature'],
            'vibration': features['vibration'],
            'pressure': features['pressure'],
            'failure_probability': prob
        }
        yield out

class WriteCsv(beam.DoFn):
    def process(self, row):
        line = f"{row['ts']},{row['device_id']},{row['temperature']},{row['vibration']},{row['pressure']},{row['failure_probability']:.4f}\n"
        with open(PRED_FILE,'a', encoding='utf-8') as f:
            f.write(line)
        # trigger alert if high
        if row['failure_probability'] > 0.8:
            send_alert(row['device_id'], row['ts'], row['failure_probability'])
        yield row

def run():
    options = PipelineOptions()
    options.view_as(PipelineOptions).streaming = True
    with beam.Pipeline(options=options) as p:
        (p
         | 'ReadSim' >> beam.io.ReadFromText('sim_input.jsonl')
         | 'Parse' >> beam.ParDo(Parse())
         | 'Score' >> beam.ParDo(Score())
         | 'Write' >> beam.ParDo(WriteCsv())
        )

if __name__ == '__main__':
    # clear output files
    if os.path.exists(PRED_FILE):
        os.remove(PRED_FILE)
    run()
