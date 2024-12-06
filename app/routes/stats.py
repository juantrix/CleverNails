from flask import Blueprint, render_template, request, Response
from app.database import query_db
from datetime import datetime
from ..utils import login_required

# Define el blueprint para las rutas relacionadas con estadísticas
stats_bp = Blueprint("stats", __name__)

@stats_bp.route("/stats", methods=["GET"])
@login_required
def stats():
    date = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
    sales = query_db("""
        SELECT s.name AS name, s.price, sa.discount, c.name AS customer_name, sa.date
        FROM sales sa
        JOIN services s ON sa.service_id = s.id
        JOIN customers c ON sa.customer_id = c.id
        WHERE sa.date LIKE ?
    """, (f"{date}%",))

    # Calcula el ingreso total considerando los descuentos
    total_revenue = sum((sale["price"] - sale["discount"]) for sale in sales) if sales else 0

    return render_template("stats.html", sales=sales, total_revenue=total_revenue, date=date)


@stats_bp.route("/download-sales", methods=["GET"])
@login_required
def download_sales():
    date = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
    sales = query_db("""
        SELECT s.name AS service_name, s.price, c.name AS customer_name, sa.date
        FROM sales sa
        JOIN services s ON sa.service_id = s.id
        JOIN customers c ON sa.customer_id = c.id
        WHERE sa.date LIKE ?
    """, (f"{date}%",))

    # Generar el CSV
    def generate_csv():
        yield "Fecha,Servicio,Precio,Cliente\n"
        for sale in sales:
            yield f"{sale['date']},{sale['service_name']},{sale['price']},{sale['customer_name']}\n"

    # Respuesta del archivo CSV
    return Response(
        generate_csv(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename=ventas_{date}.csv"}
    )
