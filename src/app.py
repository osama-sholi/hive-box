from flask import Flask, jsonify
from __version__ import VERSION

app = Flask(__name__)

# Version endpoint
@app.route('/api/version', methods=['GET'])
def get_version():
    return jsonify({"version": VERSION})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
