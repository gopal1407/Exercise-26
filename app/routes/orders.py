from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Order

order_bp = Blueprint('order_bp', __name__)

# CREATE an Order
@order_bp.route('/', methods=['POST'])
def create_order():
    data = request.json
    new_order = Order(customer_id=data['customer_id'], status=data.get('status', 'pending'))
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order created successfully", "id": new_order.id}), 201

# READ all Orders
@order_bp.route('/', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{"id": o.id, "customer_id": o.customer_id, "status": o.status} for o in orders])

# READ a single Order
@order_bp.route('/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify({"id": order.id, "customer_id": order.customer_id, "status": order.status})

# UPDATE an Order
@order_bp.route('/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    data = request.json
    order.status = data.get('status', order.status)
    db.session.commit()
    return jsonify({"message": "Order updated successfully"})

# DELETE an Order
@order_bp.route('/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted successfully"})
