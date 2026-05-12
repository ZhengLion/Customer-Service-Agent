from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from agent.state import AgentState
from agent.planner import planner_node
from agent.tool_node import tool_node
from agent.memory_node import memory_node
from agent.verifier_node import verifier_node
from langchain_core.messages import AIMessage

def responder_node(state: AgentState) -> AgentState:
    intent = state["intent"]
    tool_result = state.get("tool_result", {})
    verified = state.get("verified", False)

    if not verified:
        error = tool_result.get("error", "無法處理此請求")
        reply = f"很抱歉，無法完成您的請求：{error}"

    elif tool_result.get("remembered"):
        content = tool_result.get("content", "您的偏好")
        reply = f"好的，我已記住：「{content}」，之後的服務將依此調整。"

    elif intent == "tracking":
        if tool_result.get("repeat_issue"):
            count = tool_result.get("issue_count", 0)
            reply = f"非常抱歉，您的訂單再次出現延遲問題。我們注意到您已有 {count} 次類似問題，這次將列為優先處理，並主動聯繫您。"
        else:
            status = tool_result.get("status", "unknown")
            product = tool_result.get("product_name", "您的商品")
            reply = f"您的訂單（{product}）目前狀態為：{status}。"

    elif intent == "refund":
        order_id = tool_result.get("order_id")
        reply = f"訂單 {order_id} 的退款申請已成功送出，我們將盡快處理。"

    elif intent == "complaint":
        if tool_result.get("repeat_issue"):
            count = tool_result.get("issue_count", 0)
            reply = f"非常抱歉給您帶來不便，您的投訴已記錄。我們注意到您已有 {count} 次類似問題，這次將列為最高優先處理，並主動聯繫您。"
        else:
            reply = "您的投訴已記錄，我們將優先處理並盡快回覆您。"

    elif intent == "profile":
        name = tool_result.get("name", "客戶")
        email = tool_result.get("email", "")
        reply = f"您的帳戶資訊：姓名 {name}，Email：{email}。"

    elif intent in ("memory_read", "remember"):
        memories = tool_result.get("memory", [])
        if memories and "message" not in memories[0]:
            items = "\n".join([f"- {m['key_name']}: {m['value']}" for m in memories])
            reply = f"您的歷史記錄：\n{items}"
        else:
            reply = "目前沒有找到您的歷史記錄。"

    else:
        reply = "感謝您的聯繫，我們已收到您的訊息。"

    print(f"\n[Responder] → {reply}")
    return {"messages": [AIMessage(content=reply)]}

def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("planner", planner_node)
    builder.add_node("tool", tool_node)
    builder.add_node("memory", memory_node)
    builder.add_node("verifier", verifier_node)
    builder.add_node("responder", responder_node)

    builder.add_edge(START, "planner")
    builder.add_edge("planner", "tool")
    builder.add_edge("tool", "memory")
    builder.add_edge("memory", "verifier")
    builder.add_edge("verifier", "responder")
    builder.add_edge("responder", END)

    memory = MemorySaver()
    return builder.compile(checkpointer=memory)

graph = build_graph()

