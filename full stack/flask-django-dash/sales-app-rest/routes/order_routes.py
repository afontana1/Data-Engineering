from flask import request, jsonify

from app import app
from models.oms import Order, OrderItem


@app.route("/order")
def order():
    args = dict(request.args)
    if "order_id" in args.keys():
        order_id = args["order_id"]
        order = Order.query.get(int(order_id))
        if order:
            order.__dict__.pop("_sa_instance_state")
            return jsonify(order.__dict__)
        else:
            return jsonify({"error": "Order item not found"})
    if "order_customer_id" in args.keys():
        order_customer_id = args["order_customer_id"]
        order_recs = Order.query.filter(
            Order.order_customer_id == order_customer_id
        ).all()
        if order_recs:
            orders = []
            for order in order_recs:
                order.__dict__.pop("_sa_instance_state")
                orders.append(order.__dict__)
            return jsonify(orders)
        else:
            return jsonify({"error": "No order items found for the given order ID"})


@app.route("/order_item")
def order_item():
    args = dict(request.args)
    if "order_item_id" in args.keys():
        order_item_id = args["order_item_id"]
        order_item = OrderItem.query.get(int(order_item_id))
        if order_item:
            order_item.__dict__.pop("_sa_instance_state")
            return jsonify(order_item.__dict__)
        else:
            return jsonify({"error": "Order item not found"})
    if "order_item_order_id" in args.keys():
        order_item_order_id = args["order_item_order_id"]
        order_items = OrderItem.query.filter(
            OrderItem.order_item_order_id == order_item_order_id
        ).all()
        if order_items:
            order_items_data = []
            for order_item in order_items:
                order_item.__dict__.pop("_sa_instance_state")
                order_items_data.append(order_item.__dict__)
            return jsonify(order_items_data)
        else:
            return jsonify({"error": "No order items found for the given order ID"})
