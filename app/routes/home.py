from flask import Blueprint, render_template
from ..utils import login_required

# Define el blueprint para el índice
index_bp = Blueprint("index", __name__)


# Página principal (actual index)
@index_bp.route("/home")
@login_required
def dashboard():
    return render_template("index.html")