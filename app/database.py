import sqlite3


def query_db(query, args=(), one=False):
    conn = sqlite3.connect("manicure_shop.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, args)
    rv = cursor.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv


def initialize_db():
    # Crear tablas si no existen
    query_db("""
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL
    )
    """)
    query_db("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        birth_date TEXT,
        phone TEXT,
        email TEXT
    )
    """)
    query_db("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_id INTEGER,
        date TEXT,
        FOREIGN KEY (service_id) REFERENCES services (id)
    )
    """)

    # Verificar si la columna customer_id ya existe
    conn = sqlite3.connect("manicure_shop.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(sales)")
    columns = [column[1] for column in cursor.fetchall()]
    if "customer_id" not in columns:
        cursor.execute("ALTER TABLE sales ADD COLUMN customer_id INTEGER REFERENCES customers (id)")
        print("Columna customer_id agregada a la tabla sales.")

    if "discount" not in columns:
        cursor.execute("ALTER TABLE sales ADD COLUMN discount REAL DEFAULT 0")
        print("Columna discount agregada a la tabla sales.")

    conn.commit()
    conn.close()
