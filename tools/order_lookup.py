from tools.db_connection import get_connection

def order_lookup(order_id: int) -> dict:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
            row = cur.fetchone()
        return row if row else {"error": f"Order {order_id} not found"}
    finally:
        conn.close()
