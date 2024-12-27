import webbrowser
from functools import wraps
from flask import redirect, url_for, session
from flask_mail import Message
from app import mail
from .database import query_db

browser_opened = False


def open_browser():
    global browser_opened
    if not browser_opened:
        webbrowser.open_new("http://127.0.0.1:5000/")
        browser_opened = True


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


def get_low_stock_products():
    products = query_db("SELECT * FROM products WHERE quantity < notification_threshold")
    return products


def send_shopping_list():
    products = get_low_stock_products()
    if not products:
        return

    product_list = "\n".join([f"{p['name']}: comprar {p['notification_threshold'] - p['quantity']}" for p in products])

    msg = Message(
        "Lista de Compras - Reposición de Stock",
        sender="tuemail@example.com",
        recipients=["destinatario@example.com"]
    )
    msg.body = f"Estos son los productos que necesitas reponer:\n\n{product_list}"
    mail.send(msg)


def test_email():
    try:
        msg = Message("Prueba de correo", recipients=["juanostrit66@gmail.com"])
        msg.body = "Este es un correo de prueba."
        mail.send(msg)
        print("Correo enviado correctamente.")
        return "Correo enviado correctamente."
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return f"Error al enviar el correo: {e}"
