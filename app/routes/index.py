from flask import Blueprint, render_template

# Define el blueprint para el índice
index_bp = Blueprint("index", __name__)

@index_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")
