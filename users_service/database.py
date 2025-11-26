import sqlite3

DATABASE_NAME = "users.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            role TEXT DEFAULT 'cliente',
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()

def add_user(email, nombre, apellido, role="cliente"):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, nombre, apellido, role) VALUES (?, ?, ?, ?)",
            (email, nombre, apellido, role)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return get_user(user_id)
    except sqlite3.IntegrityError:
        conn.close()
        return None

def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE is_active = 1")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ? AND is_active = 1", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_user(user_id, email=None, nombre=None, apellido=None, role=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Solo actualiza los campos enviados
    fields = []
    values = []
    if email is not None:
        fields.append("email = ?")
        values.append(email)
    if nombre is not None:
        fields.append("nombre = ?")
        values.append(nombre)
    if apellido is not None:
        fields.append("apellido = ?")
        values.append(apellido)
    if role is not None:
        fields.append("role = ?")
        values.append(role)

    if not fields:
        conn.close()
        return None

    values.append(user_id)
    cursor.execute(f"UPDATE users SET {', '.join(fields)} WHERE id = ? AND is_active = 1", values)
    conn.commit()

    updated = get_user(user_id)
    conn.close()
    return updated

def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_active = 0 WHERE id = ?", (user_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted