from agent.state import AgentState
from tools.order_lookup import order_lookup
from tools.customer_profile import customer_profile
from tools.refund_tool import request_refund
from tools.complaint_logger import log_complaint

# 讓agent使用之前建立的那些tool，所以前面的意圖就很重要，取得用戶想幹麻之後就會有對應的tool使用

def tool_node(state: AgentState) -> AgentState:
    intent = state["intent"]
    entities = state["entities"]
    customer_id = state.get("customer_id", 1)
    order_id = entities.get("order_id")
    result = {}

    if intent == "tracking":
        if order_id:
            result = order_lookup(order_id)
        else:
            result = {"skip": True, "message": "No order_id, will check memory"}

    elif intent == "refund":
        if order_id:
            result = request_refund(order_id)
        else:
            result = {"error": "No order_id provided"}

    elif intent == "complaint":
        if order_id:
            messages = state["messages"]
            issue_text = messages[-1].content
            result = log_complaint(customer_id, order_id, issue_text)
        else:
            result = {"skip": True, "message": "No order_id, will check memory"}

    elif intent == "profile":
        result = customer_profile(customer_id)

    elif intent in ("memory_read", "remember"):
        result = {"skip": True, "message": "Will be handled by memory node"}

    else:
        result = {"error": f"Unknown intent: {intent}"}

    print(f"\n[Tool] intent={intent} → result={result}")
    return {"tool_result": result}
