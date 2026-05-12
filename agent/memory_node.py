import os
from dotenv import load_dotenv
from agent.state import AgentState
from tools.db_connection import get_connection

load_dotenv()

#這邊要處理"我以前xxxxx"的類似請求，也就是意圖會被歸類在memory_read之類的請求，要去資料庫調資料強化輸出

def memory_node(state: AgentState) -> AgentState:
    intent = state["intent"]
    customer_id = state.get("customer_id", 1)
    entities = state["entities"]
    tool_result = state.get("tool_result", {})
    messages = state["messages"]
    last_message = messages[-1].content.lower()
    if intent == "memory_read":# 如果意圖是memory_read就會近來
        conn = get_connection()# 連回資料庫
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT key_name, value FROM customer_memory WHERE customer_id = %s ORDER BY created_at DESC",
                    (customer_id,)
                )
                rows = cur.fetchall()# 將此客戶之前的所有紀錄，存入memory_result給後續節點使用
            memory_result = rows if rows else [{"message": "No memory found"}]
            print(f"\n[Memory] LTM read → {memory_result}")
            return {"tool_result": {"memory": memory_result}}
        finally:
            conn.close()
            
    remember_keywords = ["remember", "keep in mind"]#如果出現類似這種詞就記下使用者的需求
    if any(kw in last_message for kw in remember_keywords):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO customer_memory (customer_id, key_name, value) VALUES (%s, %s, %s)",
                    (customer_id, "preference", messages[-1].content)
                )
            conn.commit()
            print(f"\n[Memory] LTM write → saved user preference: {messages[-1].content}")
            return {"tool_result": {"remembered": True, "content": messages[-1].content}}
        finally:
            conn.close()
            
    if intent == "refund" and tool_result.get("success"):#如果意圖是退款且有合規定的商品的話就可以進行退款
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO customer_memory (customer_id, key_name, value) VALUES (%s, %s, %s)",
                    (customer_id, "preference", "prefers_refund_over_exchange")
                )# 紀錄此用戶偏好退款而非換貨的個性
            conn.commit()
            print(f"\n[Memory] LTM write → saved refund preference for customer {customer_id}")
        finally:
            conn.close()

    
    if intent == "complaint" and tool_result.get("success"):#如果億圖示要投訴且紀錄成功
        order_id = entities.get("order_id")
        messages = state["messages"]
        issue_text = messages[-1].content
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO customer_memory (customer_id, key_name, value) VALUES (%s, %s, %s)",
                    (customer_id, "past_issue", f"Order {order_id}: {issue_text}")
                )#將客戶最後一次輸入的投訴內容連同訂單編號存到資料庫裡面去
            conn.commit()
            print(f"\n[Memory] LTM write → saved complaint for customer {customer_id}")
        finally:
            conn.close()
            
    repeat_keywords = ["again", "always", "every time"]#如果出現重複的問題等等也要記下來
    if any(kw in last_message for kw in repeat_keywords):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT COUNT(*) as cnt FROM customer_memory WHERE customer_id = %s AND key_name = 'past_issue'",
                    (customer_id,)
                )
                row = cur.fetchone()
                issue_count = row["cnt"] if row else 0
            print(f"\n[Memory] Personalization → detected repeat complaint, past issues: {issue_count}")
            return {"tool_result": {**tool_result, "repeat_issue": True, "issue_count": issue_count}}
        finally:
            conn.close()

    return {}
