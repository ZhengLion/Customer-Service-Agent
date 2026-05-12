from tools.db_connection import get_connection

def request_refund(order_id: int) -> dict:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT status FROM orders WHERE order_id = %s", (order_id,))
            row = cur.fetchone()

            if not row:
                return {"error": f"Order {order_id} not found"}
            if row["status"] != "delivered":
                return {"error": f"Cannot refund order {order_id} (current status: {row['status']})"}

            cur.execute(
                "UPDATE orders SET status = 'refund_requested' WHERE order_id = %s",
                (order_id,)
            )
        conn.commit()
        return {"success": True, "order_id": order_id, "new_status": "refund_requested"}
    finally:
        conn.close()
