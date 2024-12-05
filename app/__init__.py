from flask import Flask
import os


def create_app():
    # Define el directorio de plantillas
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../templates"))
    app = Flask(__name__, template_folder=template_dir)

    # Importar y registrar blueprints
    from app.routes.index import index_bp
    from app.routes.customers import customers_bp
    from app.routes.services import services_bp
    from app.routes.sales import sales_bp
    from app.routes.stats import stats_bp

    app.register_blueprint(index_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(stats_bp)

    return app
