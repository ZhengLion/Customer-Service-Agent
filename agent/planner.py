import os
import json
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from agent.state import AgentState

load_dotenv()

llm = ChatOllama(model=os.getenv("LLM_MODEL", "qwen2.5:7b"), temperature=0)

SYSTEM_PROMPT = """你是一個客服 Agent 的規劃者。
根據完整對話歷史分析使用者最新的意圖，回傳 JSON 格式（不要加任何其他文字）：

{
  "intent": "<tracking|refund|complaint|profile|memory_read|remember|unknown>",
  "entities": {
    "order_id": <整數或 null>,
    "customer_id": <整數或 null>
  },
  "reason": "<簡短說明為什麼這樣判斷>"
}

重要規則：
- 如果使用者用代名詞（it, that, this order 等），請從對話歷史中找出對應的 order_id
- 意圖定義：
  - tracking：詢問訂單狀態或位置
  - refund：要求退款
  - complaint：投訴或抱怨
  - profile：查詢個人資料
  - memory_read：詢問過去的問題或歷史記錄
  - remember：使用者要求記住某個偏好（包含 remember、keep in mind、記住 等關鍵字）
  - unknown：無法判斷
"""# 規定模型 一定要選出一個意圖

def planner_node(state: AgentState) -> AgentState:
    messages = state["messages"]

    # 把完整對話歷史整理成文字給LLM參考
    history = ""
    for m in messages:
        if isinstance(m, HumanMessage):
            history += f"User: {m.content}\n"
        elif isinstance(m, AIMessage):
            history += f"Agent: {m.content}\n"

    prompt = f"對話歷史：\n{history}\n請分析最新一句 User 的意圖。"

    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ])

    try:
        result = json.loads(response.content)# 將LLM回傳的文字轉化為python dict的型態
    except json.JSONDecodeError:
        result = {"intent": "unknown", "entities": {}, "reason": "LLM 回傳格式錯誤"}

    print(f"\n[Planner] intent={result.get('intent')} entities={result.get('entities')}")
    print(f"[Planner] reason: {result.get('reason')}")

    return {
        "intent": result.get("intent", "unknown"),
        "entities": result.get("entities", {}),
        "tool_result": {},
        "verified": False,#這邊設為false因為驗證是由驗證節點來處理，這邊只要整理使用者需求並歸化就好
    }
