from agent.state import AgentState

# 此階段要用來驗證tool有沒有用對或是記憶節點的結果有沒有符合邏輯等等，確保不要輸出錯誤訊息

def verifier_node(state: AgentState) -> AgentState:
    tool_result = state.get("tool_result", {})
    intent = state["intent"]


    if "error" in tool_result:#如果有任何error在tool result就直接重來
        print(f"\n[Verifier] X_X FAILED → {tool_result['error']}")
        return {"verified": False}

    if tool_result.get("remembered"):
        print(f"\n[Verifier] ^_^ PASSED (preference saved)")
        return {"verified": True}
    if tool_result.get("repeat_issue"):
     
        print(f"\n[Verifier] ^_^ PASSED (repeat issue detected)")
        return {"verified": True}
    if intent == "memory_read" and "memory" in tool_result:# 如果意圖是memory read的話結果裡面就要包含memory
        print(f"\n[Verifier] ^_^ PASSED (memory_read)")
        return {"verified": True}

    
    if intent in ("refund", "complaint"):# 退款以及抱怨的意圖要有success的結論才算過
        passed = tool_result.get("success", False)
        print(f"\n[Verifier] {'V PASSED' if passed else 'X_X FAILED'} ({intent})")
        return {"verified": passed}

    
    if tool_result and "error" not in tool_result:# 追蹤訂單跟查詢個人資料，有資料就通過
        print(f"\n[Verifier] ^_^ PASSED ({intent})")
        return {"verified": True}
        


    print(f"\n[Verifier] X_X FAILED (no result)")
    return {"verified": False}
