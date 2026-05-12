from langchain_core.messages import HumanMessage
from agent.graph import graph

def run(query, session_id="session-1", customer_id=1):
    config = {"configurable": {"thread_id": session_id}}
    result = graph.invoke(
        {"messages": [HumanMessage(content=query)], "customer_id": customer_id},
        config=config
    )
    print(f"User:  {query}")
    print(f"Agent: {result['messages'][-1].content}")
    print()
    return result

print("=" * 60)
print("Test #1 — Intent Parsing")
print("Expected: Extract intent=tracking, order_id")
print("=" * 60)
run("Where is my order 12345?", session_id="test1")

print("=" * 60)
print("Test #2 — OrderLookupTool")
print("Expected: Query MySQL orders table")
print("=" * 60)
run("Check status of order 1001", session_id="test2")

print("=" * 60)
print("Test #3 — CustomerProfileTool")
print("Expected: Retrieve customer info")
print("=" * 60)
run("Show my profile", session_id="test3")

print("=" * 60)
print("Test #4 — RefundTool")
print("Expected: Update order status")
print("=" * 60)
run("Refund order 5678", session_id="test4")

print("=" * 60)
print("Test #5 — ComplaintLoggerTool")
print("Expected: Insert complaint record")
print("=" * 60)
run("I want to complain about order 2222", session_id="test5", customer_id=2)

print("=" * 60)
print("Test #6 — Multi-step Reasoning")
print("Expected: Check then perform refund")
print("=" * 60)
run("Refund order 7890 if delivered", session_id="test6")

print("=" * 60)
print("Test #7 — Short-Term Memory (STM)")
print("Expected: Use previous order_id")
print("=" * 60)
run("Where is my order 1001?", session_id="test7")
run("Cancel it", session_id="test7")

print("=" * 60)
print("Test #8 — Long-Term Memory Read")
print("Expected: Retrieve from memory")
print("=" * 60)
run("What issues have I had before?", session_id="test8")

print("=" * 60)
print("Test #9 — Long-Term Memory Write")
print("Expected: Save preference to customer_memory")
print("=" * 60)
run("Remember I prefer refunds", session_id="test9")

print("=" * 60)
print("Test #10 — Personalization")
print("Expected: Detect repeated issue")
print("=" * 60)
run("My order is late again", session_id="test10")

print("=" * 60)
print("Test #11 — Verifier")
print("Expected: Reject invalid order")
print("=" * 60)
run("Refund order 0000", session_id="test11")
