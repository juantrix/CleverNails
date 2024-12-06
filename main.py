from app.database import initialize_db
from app import create_app


app = create_app()


for rule in app.url_map.iter_rules():
    print(rule)


if __name__ == "__main__":
    # Inicializar la base de datos
    initialize_db()

    # Ejecutar la aplicación
    app.run(debug=False)
