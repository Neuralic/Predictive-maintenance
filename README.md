# Predictive Maintenance — Real-Time Equipment Failure Prediction (Neuralic)

** GCP-native prototype** showing streaming IoT ingestion, real-time
enrichment, and model-based scoring using Google Cloud patterns (Pub/Sub → Dataflow → BigQuery → Vertex AI).
This repo is authored and organized by Neuralic as a production-style demo.

## Summary
This project simulates multiple industrial sensors producing telemetry. The pipeline ingests
sensor events, normalizes values, computes rolling features, and scores each record with a
predictive model. Records with high failure risk trigger an alert (simulated webhook/log).

## Demo mapping to GCP
- Replace `sim_input.jsonl` and local components with `beam.io.ReadFromPubSub(...)` to ingest from Pub/Sub.
- Run `dataflow_pipeline.py` with DataflowRunner to execute on Cloud Dataflow.
- Replace local CSV writes with `beam.io.WriteToBigQuery(...)` to persist into BigQuery.
- Replace `mock_vertex_predict()` calls with Vertex AI online prediction calls or Vertex endpoints.

## Files
- `publisher.py` — sensor simulator that writes to `sim_input.jsonl` (demo Pub/Sub)
- `dataflow_pipeline.py` — Apache Beam pipeline (local/demo mode)
- `vertex_model.py` — prediction helper (mocked Vertex AI behavior)
- `alerter.py` — sends simulated alerts (prints / webhook stub)
- `config.yaml` — placeholder GCP config values
- `schemas/bigquery_schema.json` — BigQuery table schema
- `requirements.txt` — Python dependencies

## Quick local demo
1. Create Python 3.11 virtualenv and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
2. Start the demo data publisher:
   ```bash
   python publisher.py
   ```
   This writes `sim_input.jsonl` with streaming sensor events.
3. Run the pipeline (in another terminal):
   ```bash
   python dataflow_pipeline.py
   ```
   The pipeline consumes `sim_input.jsonl` and writes `output/predictions.csv` and `output/alerts.log`.

## Author
Neuralic — Machine Learning & AI Automation

## Notes for clients
This is a production-pattern prototype. Neuralic can deploy this end-to-end on your GCP environment,
replacing demo inputs with Pub/Sub, using DataflowRunner, and deploying models to Vertex AI for robust
online scoring.
