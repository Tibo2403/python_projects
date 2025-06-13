import json
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_BASE = "https://data.mobility.brussels/traffic/api/counts/"


def fetch_data(feature_id=None, start_date=None, end_date=None):
    """Fetch counts from Mobility.Brussels API.

    If a date range is provided, the history endpoint is used, otherwise the live
    endpoint is called.
    """
    if feature_id and start_date and end_date:
        url = (
            f"{API_BASE}?request=history&featureID={feature_id}"
            f"&startDate={start_date}&endDate={end_date}"
        )
    else:
        url = f"{API_BASE}?request=live"
    resp = requests.get(url, timeout=10)
    return resp.json()


def filter_features(features, name=None, equipment=None, zone=None):
    """Filter the list of features according to optional criteria."""
    result = []
    for f in features:
        props = f.get("properties", {})
        if name and name.lower() not in str(props.get("name", "")).lower():
            continue
        if equipment and equipment.lower() not in str(props.get("equipment", "")).lower():
            continue
        if zone and zone.lower() not in str(props.get("zone", "")).lower():
            continue
        result.append(f)
    return result

@app.route("/")
def index():
    """Render map with optional filtering based on query parameters."""
    feature_id = request.args.get("feature_id")
    name = request.args.get("name")
    equipment = request.args.get("equipment")
    zone = request.args.get("zone")
    start = request.args.get("start_date")
    end = request.args.get("end_date")

    data = {}
    try:
        data = fetch_data(feature_id, start, end)
        if data.get("features"):
            data["features"] = filter_features(
                data["features"], name=name, equipment=equipment, zone=zone
            )
    except Exception:
        # In case of network issues or wrong parameters, return empty dataset
        data = {}

    return render_template("index.html", data=json.dumps(data))

if __name__ == "__main__":
    app.run(debug=True)
