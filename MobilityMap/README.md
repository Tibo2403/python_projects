# MobilityMap

Simple Flask application displaying live pedestrian and vehicle traffic from Mobility.Brussels on an interactive map.

## Setup

Create a virtual environment and install requirements:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```
Then open `http://localhost:5000` in your browser.

You can provide query parameters to filter the displayed data:

```
http://localhost:5000?feature_id=123&name=station&equipment=camera&zone=center&start_date=20240101&end_date=20240131
```

Parameters are optional and allow filtering by detector ID or name, equipment
type, zone and a date range (using the API history endpoint).
