from flask import Blueprint, request, jsonify, render_template
from app.database import query_db

# Define el blueprint para la gestión de stock
stock_bp = Blueprint("stock", __name__)


@stock_bp.route("/products", methods=["GET"])
def get_products():
    # Obtener el parámetro de búsqueda
    search = request.args.get("search", "").strip()

    if search:
        products = query_db(
            "SELECT * FROM products WHERE name LIKE ?",
            (f"%{search}%",)
        )
    else:
        products = query_db("SELECT * FROM products")

    return jsonify([{
        "id": product["id"],
        "name": product["name"],
        "price": product["price"],
        "quantity": product["quantity"],
        "notification_threshold": product["notification_threshold"] if "notification_threshold" in product else 0
    } for product in products])


@stock_bp.route("/products/manage", methods=["GET"])
def manage_products_page():
    # Renderizar la página de gestión de stock
    return render_template("manage_stock.html")


@stock_bp.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    name = data.get("name")
    price = data.get("price")
    quantity = data.get("quantity")
    notification_threshold = data.get("notification_threshold", 0)

    if not name or price is None or quantity is None:
        return jsonify({"error": "Todos los campos son obligatorios."}), 400

    query_db(
        "INSERT INTO products (name, price, quantity, notification_threshold) VALUES (?, ?, ?, ?)",
        (name, float(price), int(quantity), int(notification_threshold))
    )
    return jsonify({"message": "Producto agregado exitosamente."}), 201


@stock_bp.route("/products/notification", methods=["PUT"])
def update_notification_threshold():
    data = request.get_json()
    product_id = data.get("id")
    threshold = data.get("threshold")

    # Validación
    if not product_id or threshold is None:
        return jsonify({"error": "ID del producto y el nivel de notificación son obligatorios."}), 400

    # Actualización en la base de datos
    try:
        print(f"Actualizando producto {product_id} con threshold {threshold}")
        query_db(
            "UPDATE products SET notification_threshold = ? WHERE id = ?",
            (10, int(product_id))
        )
        return jsonify({"message": "Nivel de notificación actualizado exitosamente."}), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar la base de datos: {e}"}), 500


@stock_bp.route("/products", methods=["PUT"])
def update_product():
    # Actualizar cantidad de un producto
    data = request.get_json()
    product_id = data.get("id")
    change = data.get("change")

    if not product_id or change is None:
        return jsonify({"error": "ID del producto y cambio son obligatorios."}), 400

    query_db(
        "UPDATE products SET quantity = quantity + ? WHERE id = ?",
        (int(change), int(product_id))
    )
    return jsonify({"message": "Cantidad actualizada exitosamente."}), 200


@stock_bp.route("/products", methods=["DELETE"])
def delete_product():
    # Eliminar un producto
    data = request.get_json()
    product_id = data.get("id")

    if not product_id:
        return jsonify({"error": "ID del producto es obligatorio."}), 400

    query_db("DELETE FROM products WHERE id = ?", (int(product_id),))
    return jsonify({"message": "Producto eliminado exitosamente."}), 200
