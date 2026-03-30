from flask import Flask, request, jsonify
from flask_cors import CORS
import database
import json

app = Flask(__name__)
CORS(app)

# INIT DB
database.init_db()

# ======================
# REGISTER CUSTOMER
# ======================
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data['name']
    contact = data['contact']

    database.insert_customer(name, contact)
    user = database.get_customer(contact)

    return jsonify({"status": "success", "user": user})


# ======================
# CHECK CUSTOMER
# ======================
@app.route('/check', methods=['POST'])
def check():
    contact = request.json['contact']
    user = database.get_customer(contact)

    return jsonify({"exists": user is not None})


# ======================
# PLACE ORDER
# ======================
@app.route('/order', methods=['POST'])
def order():
    data = request.json
    customer_id = data['customer_id']
    items = json.dumps(data['items'])
    total = data['total']

    database.insert_order(customer_id, items, total)

    return jsonify({"status": "order placed"})


# ======================
# GET ALL ORDERS (CASHIER)
# ======================
@app.route('/orders')
def orders():
    data = database.get_orders()

    orders = []
    for o in data:
        orders.append({
            "id": o[0],
            "total": o[3],
            "status": o[4]
        })

    return jsonify(orders)


# ======================
# COMPLETE ORDER
# ======================
@app.route('/complete/<int:id>', methods=['POST'])
def complete(id):
    database.complete_order(id)
    return jsonify({"status": "done"})


# ======================
# RUN SERVER
# ======================
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)