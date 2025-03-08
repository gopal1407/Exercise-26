from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Customer

customer_bp = Blueprint('customer_bp', __name__)

# CREATE a new Customer
@customer_bp.route('/', methods=['POST'])
def create_customer():
    data = request.json
    new_customer = Customer(name=data['name'], email=data['email'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "Customer created successfully", "id": new_customer.id}), 201

# READ all Customers
@customer_bp.route('/', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{"id": c.id, "name": c.name, "email": c.email} for c in customers])

# READ a single Customer
@customer_bp.route('/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify({"id": customer.id, "name": customer.name, "email": customer.email})

# UPDATE a Customer
@customer_bp.route('/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    data = request.json
    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    db.session.commit()
    return jsonify({"message": "Customer updated successfully"})

# DELETE a Customer
@customer_bp.route('/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted successfully"})
