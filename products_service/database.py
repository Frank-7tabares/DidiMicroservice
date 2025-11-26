import sqlite3

DATABASE_NAME = "products.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            descripcion TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_product(nombre, precio, descripcion):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (nombre, precio, descripcion) VALUES (?, ?, ?)",
        (nombre, precio, descripcion)
    )
    conn.commit()
    product_id = cursor.lastrowid
    conn.close()
    return get_product(product_id)

def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_product(product_id, nombre=None, precio=None, descripcion=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Solo actualiza los campos enviados
    fields = []
    values = []
    if nombre is not None:
        fields.append("nombre = ?")
        values.append(nombre)
    if precio is not None:
        fields.append("precio = ?")
        values.append(precio)
    if descripcion is not None:
        fields.append("descripcion = ?")
        values.append(descripcion)

    if not fields:
        conn.close()
        return None

    values.append(product_id)
    cursor.execute(f"UPDATE products SET {', '.join(fields)} WHERE id = ?", values)
    conn.commit()

    updated = get_product(product_id)
    conn.close()
    return updated

def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted