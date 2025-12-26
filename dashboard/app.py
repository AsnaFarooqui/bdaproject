from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

MONGO_URI = "mongodb://mongo:27017"
client = MongoClient(MONGO_URI)

db = client["bda_project"]
kpi_col = db["kpi_minute"]


# ------------------------
# Dashboard UI Page
# ------------------------
@app.route("/")
def dashboard_home():
    return render_template("dashboard.html")


# --------------------------
# REST API Endpoints
# --------------------------
@app.route("/kpi/latest")
def get_latest_kpi():
    doc = kpi_col.find_one(sort=[("minute", -1)])
    return jsonify(doc or {})


@app.route("/kpi/data")
def get_kpi_data():
    category = request.args.get("category")
    state = request.args.get("state")

    query = {}

    if category:
        query["product_category"] = category

    if state:
        query["customer_state"] = state

    docs = list(kpi_col.find(query).sort("minute", -1).limit(200))

    for d in docs:
        d["_id"] = str(d["_id"])
        d["minute"] = d["minute"].isoformat()

    return jsonify(docs)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



