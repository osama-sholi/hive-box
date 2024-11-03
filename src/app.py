"""
This module contains the API endpoints and metrics for the application.
"""
import time
import os
import json
import valkey
from flask import Flask, jsonify, request 
from prometheus_client import CollectorRegistry, generate_latest, Counter, Histogram
from dotenv import load_dotenv
from src.get_boxes import get_boxes
from src.get_temp_avg import get_temp_avg
from __version__ import VERSION

app = Flask(__name__)

# Create a registry to hold metrics
registry = CollectorRegistry()

# Define metrics
REQUEST_COUNT = Counter('request_count', 'Total number of requests', ['method', 'endpoint'], registry=registry)
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Histogram of request latencies', ['method', 'endpoint'], registry=registry)

# Valkey configuration
load_dotenv()
host = os.getenv('VALKEY_HOST')
port = int(os.getenv('VALKEY_PORT'))
valk = valkey.Valkey(host=host, port=port, db=0)

# Version endpoint
@app.route('/api/version', methods=['GET'])
def get_version():
    """
    Return the version of the API
    """
    return jsonify({"version": VERSION})

# Average temperature endpoint
@app.route('/api/temperature', methods=['GET'])
def get_temperature():
    """
    Return the average temperature of all boxes one hour ago
    """
    # Check if the output is in the cache
    cached_output = valk.get("temperature")
    if cached_output is not None:
        # Return cached output as JSON
        return jsonify(json.loads(cached_output))

    # Retrieve and calculate temperature data if not cached
    boxes = get_boxes()
    if boxes is not None:
        temp_avg = get_temp_avg(boxes)

        if temp_avg is None:
            return jsonify({"error": "Unable to get temperature"}), 500
        else:
            # Determine the status based on the average temperature
            if temp_avg < 10:
                status = "Too Cold"
            elif 11 <= temp_avg <= 36:
                status = "Good"
            else:
                status = "Too Hot"

            output = r'{"average_temperature": ' + str(temp_avg) + r', "status": "' + status + r'"}'
            # Add the output to the cache as a JSON string
            valk.set("temperature", output, ex=300)
            return jsonify(json.loads(output))
    else:
        return jsonify({"error": "Unable to get temperature"}), 500

# Metrics endpoint
@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """
    Return the metrics of the API
    """
    # Record the request
    REQUEST_COUNT.labels(method='GET', endpoint='/metrics').inc()
    return generate_latest(registry), 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}

# readyz endpoint
@app.route('/api/readyz', methods=['GET'])
def get_readyz():
    """
    Return HTTP 200 OK to indicate the service is ready
    unless caching content is older than 5 min.
    """
    # Check if the cache is older than 5 minutes
    if valk.get("temperature") is None:
        return jsonify({"ready": False, "reason": "Cache is empty"}), 503

    return jsonify({"ready": True})

# Middleware to track request latency
@app.before_request
def start_timer():
    app.start_time = time.time()

@app.after_request
def record_request(response):
    latency = time.time() - app.start_time
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.path).observe(latency)
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
