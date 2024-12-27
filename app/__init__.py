from flask import Flask
import os
from flask_mail import Mail

mail = Mail()
PASS = '0311'


def create_app():
    # Define el directorio de plantillas
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../templates"))
    app = Flask(__name__, template_folder=template_dir)

    # Configuración de Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'clveverbot@gmail.com'
    app.config['MAIL_PASSWORD'] = 'ucvzridrfruivras'
    app.config['MAIL_DEFAULT_SENDER'] = ('Clever Nails', 'clveverbot@gmail.com')


    # Inicializar extensiones
    mail.init_app(app)

    # Importar y registrar blueprints
    from app.routes.home import index_bp
    from app.routes.customers import customers_bp
    from app.routes.services import services_bp
    from app.routes.sales import sales_bp
    from app.routes.stats import stats_bp
    from app.routes.index import auth_bp
    from app.routes.stock import stock_bp

    app.register_blueprint(index_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(stock_bp)

    app.secret_key = '123456'

    return app
