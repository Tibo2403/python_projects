import json
from flask import Flask, render_template
import requests

app = Flask(__name__)

API_URL = "https://data.mobility.brussels/traffic/api/counts/?request=live"

@app.route("/")
def index():
    try:
        resp = requests.get(API_URL, timeout=10)
        data = resp.json()
    except Exception:
        data = {}
    return render_template("index.html", data=json.dumps(data))

if __name__ == "__main__":
    app.run(debug=True)
