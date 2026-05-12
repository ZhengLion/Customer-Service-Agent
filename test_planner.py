from langchain_core.messages import HumanMessage
from agent.graph import graph

#整合測試

config = {"configurable": {"thread_id": "test-session-1"}}# 將此次對話紀錄成一個id方便短期記憶存取

test_queries = [
    "Where is my order 12345?",
    "I want a refund for order 5678",
    "I want to complain about order 2222",
    "Show my profile",
    "What issues have I had before?",
]# 測試資料集同步project的要求

for query in test_queries:
    print(f"\n{'='*50}")
    print(f"User: {query}")
    result = graph.invoke(
        {"messages": [HumanMessage(content=query)], "customer_id": 1},
        config=config
    )#模擬用戶再問問題 然後手動設定用戶是一號（seed.py裡面預設的Alice Chen）
    print(f"Intent:   {result['intent']}")# 顯示用戶想知道的東西（意圖）
    print(f"Entities: {result['entities']}")# 實體
