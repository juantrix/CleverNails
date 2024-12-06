from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from .. import PASS

# Crear el blueprint para autenticación
auth_bp = Blueprint("auth", __name__)


# Ruta para el login
@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # username = request.form.get("username")
        username = "admin"
        password = request.form.get("password")
        print("user", username)
        print('pass', password)
        # Validar credenciales (puedes cambiar esto por una base de datos u otro sistema)
        if username == "admin" and password == PASS:
            session["logged_in"] = True
            return redirect("/home")  # Redirigir al dashboard principal
        else:
            flash("Credenciales inválidas. Intenta de nuevo.", "danger")

    return render_template("login.html")


# Ruta para cerrar sesión
@auth_bp.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("auth.login"))
