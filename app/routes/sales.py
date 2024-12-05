from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.database import query_db
from datetime import datetime

# Define el blueprint para las rutas relacionadas con las ventas
sales_bp = Blueprint("sales", __name__)

@sales_bp.route("/sales", methods=["GET", "POST"])
def sales():
    if request.method == "POST":
        client_id = request.form.get("client_id")
        service_id = request.form.get("service_id")
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if client_id and service_id:
            query_db("INSERT INTO sales (service_id, customer_id, date) VALUES (?, ?, ?)", 
                     (int(service_id), int(client_id), date))
        return redirect(url_for("sales.sales"))  # Especifica el endpoint del blueprint
    services = query_db("SELECT * FROM services")
    customers = query_db("SELECT * FROM customers")
    return render_template("sales.html", services=services, customers=customers)

@sales_bp.route("/register-sale", methods=["POST"])
def register_sale():
    data = request.get_json()

    # Depuración: imprime los datos recibidos
    print("Datos recibidos:", data)

    customer_id = data.get("client_id")
    services = data.get("services", [])
    quantities = data.get("quantities", [])  # Cantidades asociadas a cada servicio

    # Validaciones
    if not customer_id:
        return jsonify({"success": False, "message": "El cliente es obligatorio."}), 400
    if not services or not quantities or len(services) != len(quantities):
        return jsonify({"success": False, "message": "Debes seleccionar al menos un servicio y especificar una cantidad válida."}), 400

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Registrar servicios con cantidades en la base de datos
    for service_id, quantity in zip(services, quantities):
        for _ in range(int(quantity)):
            query_db(
                "INSERT INTO sales (service_id, customer_id, date) VALUES (?, ?, ?)",
                (service_id, customer_id, date),
            )

    return jsonify({"success": True, "message": "Venta registrada exitosamente."}), 200
