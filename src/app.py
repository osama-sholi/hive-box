from flask import Flask, jsonify
from src.get_boxes import get_boxes
from src.get_temp_avg import get_temp_avg
from __version__ import VERSION

app = Flask(__name__)

# Version endpoint
@app.route('/api/version', methods=['GET'])
def get_version():
    """
    Return the version of the API
    """
    return jsonify({"version": VERSION})

# Avarage temperature endpoint
@app.route('/api/temperature', methods=['GET'])
def get_temperature():
    """
    Return the average temperature of all boxes one hour ago
    """
    boxes = get_boxes()
    if boxes is not None:
        temp_avg = get_temp_avg(boxes)

        if temp_avg is None:
            return jsonify({"error": "Unable to get temperature"}), 500
        else:
            return jsonify({"temperature": temp_avg})  
    else:
        return jsonify({"error": "Unable to get temperature"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
