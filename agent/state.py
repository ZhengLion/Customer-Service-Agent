from typing import Annotated
from langgraph.graph import MessagesState

# 定義agent的"特性"or"資訊"總共會有以下這幾個

class AgentState(MessagesState):
    intent: str
    entities: dict
    tool_result: dict
    verified: bool
    customer_id: int
