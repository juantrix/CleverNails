from app.database import initialize_db
from app import create_app
from flask_mail import Mail
from app.utils import send_shopping_list, test_email
from apscheduler.schedulers.background import BackgroundScheduler


app = create_app()
mail = Mail(app)

if __name__ == "__main__":
    # Inicializar la base de datos
    initialize_db()
    with app.app_context():
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=send_shopping_list, trigger="interval", weeks=1)
        scheduler.start()
        send_shopping_list()
    # Ejecutar la aplicación
    app.run(debug=False)
