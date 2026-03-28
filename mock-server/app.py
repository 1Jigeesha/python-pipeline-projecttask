from flask import Flask, jsonify, request, abort
import json
import os

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "customers.json")
with open(DATA_FILE, "r", encoding="utf-8") as f:
    customers = json.load(f)


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/customers")
def list_customers():
    try:
        page = max(int(request.args.get("page", 1)), 1)
    except ValueError:
        page = 1
    try:
        limit = max(int(request.args.get("limit", 10)), 1)
    except ValueError:
        limit = 10

    start = (page - 1) * limit
    end = start + limit
    sliced = customers[start:end]

    return jsonify({
        "data": sliced,
        "total": len(customers),
        "page": page,
        "limit": limit,
    })


@app.route("/api/customers/<customer_id>")
def get_customer(customer_id):
    cust = next((c for c in customers if str(c.get("customer_id")) == str(customer_id)), None)
    if not cust:
        abort(404)
    return jsonify({"data": cust})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
