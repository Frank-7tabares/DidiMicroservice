import sqlite3
from datetime import datetime
import logging

DATABASE_NAME = "orders.db"

logger = logging.getLogger(__name__)


def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error de conexión a la base de datos: {str(e)}")
        raise


def create_tables():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Tabla de órdenes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                direccion_entrega TEXT NOT NULL,
                total REAL NOT NULL,
                estado TEXT NOT NULL DEFAULT 'pendiente',
                fecha_creacion TEXT NOT NULL,
                CHECK (total > 0),
                CHECK (user_id > 0)
            )
        ''')

        # Tabla de items de orden
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                CHECK (cantidad > 0 AND cantidad <= 100),
                CHECK (precio_unitario > 0),
                CHECK (product_id > 0)
            )
        ''')

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logger.error(f"Error al crear tablas: {str(e)}")
        raise


def add_order(user_id, direccion_entrega, total, items):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Validaciones antes de insertar
        if user_id <= 0:
            raise ValueError("ID de usuario inválido")
        if total <= 0:
            raise ValueError("Total debe ser mayor a 0")
        if not items:
            raise ValueError("La orden debe tener items")

        fecha_creacion = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO orders (user_id, direccion_entrega, total, estado, fecha_creacion) VALUES (?, ?, ?, ?, ?)",
            (user_id, direccion_entrega, total, "pendiente", fecha_creacion)
        )
        order_id = cursor.lastrowid

        # Insertar items
        for item in items:
            if item["cantidad"] <= 0 or item["cantidad"] > 100:
                raise ValueError("Cantidad debe estar entre 1 y 100")
            if item["precio_unitario"] <= 0:
                raise ValueError("Precio unitario debe ser mayor a 0")

            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, cantidad, precio_unitario) VALUES (?, ?, ?, ?)",
                (order_id, item["product_id"], item["cantidad"], item["precio_unitario"])
            )

        conn.commit()
        conn.close()
        return get_order(order_id)
    except Exception as e:
        conn.rollback()
        conn.close()
        logger.error(f"Error al agregar orden: {str(e)}")
        return None


# Las demás funciones (get_orders, get_orders_by_user, etc.) permanecen igual pero con logging
def get_orders():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders ORDER BY fecha_creacion DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error(f"Error al obtener órdenes: {str(e)}")
        raise


def get_orders_by_user(user_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY fecha_creacion DESC", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error(f"Error al obtener órdenes del usuario {user_id}: {str(e)}")
        raise


def get_order(order_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    except Exception as e:
        logger.error(f"Error al obtener orden {order_id}: {str(e)}")
        raise


def get_order_items(order_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error(f"Error al obtener items de orden {order_id}: {str(e)}")
        raise


def update_order(order_id, estado=None, direccion_entrega=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        fields = []
        values = []
        if estado is not None:
            fields.append("estado = ?")
            values.append(estado)
        if direccion_entrega is not None:
            fields.append("direccion_entrega = ?")
            values.append(direccion_entrega)

        if not fields:
            conn.close()
            return None

        values.append(order_id)
        cursor.execute(f"UPDATE orders SET {', '.join(fields)} WHERE id = ?", values)
        conn.commit()

        updated = get_order(order_id)
        conn.close()
        return updated
    except Exception as e:
        logger.error(f"Error al actualizar orden {order_id}: {str(e)}")
        raise


def delete_order(order_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted
    except Exception as e:
        logger.error(f"Error al eliminar orden {order_id}: {str(e)}")
        raise