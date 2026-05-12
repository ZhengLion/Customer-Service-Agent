from tools.db_connection import get_connection

def customer_profile(customer_id: int) -> dict:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
            row = cur.fetchone()
        return row if row else {"error": f"Customer {customer_id} not found"}
    finally:
        conn.close()
