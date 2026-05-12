from tools.db_connection import get_connection

def log_complaint(customer_id: int, order_id: int, issue: str) -> dict:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO complaints (customer_id, order_id, issue) VALUES (%s, %s, %s)",
                (customer_id, order_id, issue)
            )
        conn.commit()
        return {"success": True, "message": "Complaint logged successfully"}
    finally:
        conn.close()
