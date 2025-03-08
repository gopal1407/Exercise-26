from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Product

product_bp = Blueprint('product_bp', __name__)

# CREATE a Product
@product_bp.route('/', methods=['POST'])
def create_product():
    data = request.json
    new_product = Product(name=data['name'], price=data['price'], stock=data['stock'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product created successfully", "id": new_product.id}), 201

# READ all Products
@product_bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock} for p in products])

# READ a single Product
@product_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"id": product.id, "name": product.name, "price": product.price, "stock": product.stock})

# UPDATE a Product
@product_bp.route('/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    data = request.json
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)
    db.session.commit()
    return jsonify({"message": "Product updated successfully"})

# DELETE a Product
@product_bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})
