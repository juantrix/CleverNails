# app/routes/customers.py
from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from app.database import query_db

# Define el blueprint
customers_bp = Blueprint("customers", __name__)


@customers_bp.route("/customers", methods=["GET"])
def customers():
    query = request.args.get("search", "")
    if query:
        customers = query_db("SELECT * FROM customers WHERE name LIKE ?", ('%' + query + '%',))
    else:
        customers = query_db("SELECT * FROM customers")
    return render_template("customers.html", customers=customers)


@customers_bp.route("/customer/<int:customer_id>")
def customer_details(customer_id):
    # Obtener el cliente
    customer = query_db("SELECT * FROM customers WHERE id = ?", (customer_id,), one=True)
    if not customer:
        return "Cliente no encontrado", 404

    # Obtener historial de servicios, incluyendo el descuento
    services = query_db("""
        SELECT s.name AS service_name, s.price, sa.discount, sa.date
        FROM sales sa
        JOIN services s ON sa.service_id = s.id
        WHERE sa.customer_id = ?
        ORDER BY sa.date DESC
    """, (customer_id,))

    # Calcular el total gastado, considerando los descuentos
    total_spent = sum(service['price'] - (service['discount'] or 0) for service in services)
    print(total_spent)

    return render_template(
        "customer_details.html", 
        customer=customer, 
        services=services, 
        total_spent=total_spent
    )


@customers_bp.route("/register-customer", methods=["GET", "POST"])
def register_customer():
    if request.method == "POST":
        name = request.form.get("name")
        birth_date = request.form.get("birth_date")
        phone = request.form.get("phone")
        email = request.form.get("email")

        if not name or not phone or not email:
            return render_template(
                "register_customer.html",
                error="El nombre, el teléfono y el correo electrónico son obligatorios."
            )

        query_db(
            "INSERT INTO customers (name, birth_date, phone, email) VALUES (?, ?, ?, ?)",
            (name, birth_date, phone, email)
        )

        return render_template(
            "register_customer.html",
            success="Cliente registrado exitosamente."
        )

    return render_template("register_customer.html")


@customers_bp.route("/search-customers", methods=["GET"])
def search_customers():
    query = request.args.get("query", "").strip()
    if query:
        customers = query_db("SELECT id, name, email FROM customers WHERE name LIKE ?", (f"%{query}%",))
        return jsonify([{"id": customer["id"], "name": customer["name"], "email": customer["email"]} for customer in customers])
    return jsonify([])


@customers_bp.route("/delete-customer/<int:customer_id>", methods=["POST"])
def delete_customer(customer_id):
    # Verificar si el cliente existe
    customer = query_db("SELECT * FROM customers WHERE id = ?", (customer_id,), one=True)
    if not customer:
        return "Cliente no encontrado", 404

    # Eliminar el cliente de la base de datos
    query_db("DELETE FROM customers WHERE id = ?", (customer_id,))
    return redirect(url_for("customers.customers"))


@customers_bp.route("/edit-customer/<int:customer_id>", methods=["GET", "POST"])
def edit_customer(customer_id):
    # Obtener el cliente actual desde la base de datos
    customer = query_db("SELECT * FROM customers WHERE id = ?", (customer_id,), one=True)
    if not customer:
        return "Cliente no encontrado", 404

    if request.method == "POST":
        # Obtener datos del formulario
        name = request.form.get("name")
        birth_date = request.form.get("birth_date")
        phone = request.form.get("phone")
        email = request.form.get("email")

        # Validar los campos obligatorios
        if not name or not phone or not email:
            return render_template(
                "edit_customer.html",
                customer=customer,
                error="El nombre, el teléfono y el correo electrónico son obligatorios."
            )

        # Actualizar el cliente en la base de datos
        query_db(
            "UPDATE customers SET name = ?, birth_date = ?, phone = ?, email = ? WHERE id = ?",
            (name, birth_date, phone, email, customer_id)
        )

        # Redirigir a la lista de clientes después de la edición
        return redirect(url_for("customers.customers"))

    # Renderizar el formulario con los datos actuales
    return render_template("edit_customer.html", customer=customer)
