"""Mock Vertex AI predictor helper.
In production, replace `mock_vertex_predict` with an actual Vertex AI online prediction call
using google-cloud-aiplatform client and your deployed endpoint.
"""
import math

def mock_vertex_predict(features: dict) -> float:
    """Return a failure probability between 0 and 1 using a simple heuristic.
    Features expects temperature, vibration, pressure.
    This mimics a trained model for demo purposes.
    """
    temp = features.get('temperature', 0.0)
    vib = features.get('vibration', 0.0)
    pres = features.get('pressure', 0.0)

    # simple heuristic: high temp and high vibration => higher failure prob
    score = 0.0
    score += max(0, (temp - 60.0) / 60.0) * 0.6
    score += max(0, (vib - 1.5) / 3.0) * 0.3
    score += max(0, (pres - 8.0) / 4.0) * 0.1
    # clamp
    prob = 1.0 / (1.0 + math.exp(-10*(score - 0.4)))  # sigmoid sharpness
    return float(min(max(prob, 0.0), 1.0))
