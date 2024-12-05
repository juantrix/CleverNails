from flask import Blueprint, render_template, request, redirect, url_for
from app.database import query_db

# Define el blueprint para los servicios
services_bp = Blueprint("services", __name__)

@services_bp.route("/services", methods=["GET", "POST"])
def services():
    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        if name and price:
            query_db("INSERT INTO services (name, price) VALUES (?, ?)", (name, float(price)))
        return redirect(url_for("services.services"))  # Especifica el endpoint del blueprint
    services = query_db("SELECT * FROM services")
    return render_template("services.html", services=services)

@services_bp.route("/delete-service", methods=["POST"])
def delete_service():
    service_id = request.form.get("service_id")
    if service_id:
        query_db("DELETE FROM services WHERE id = ?", (service_id,))
    return redirect(url_for("services.services"))  # Especifica el endpoint del blueprint
