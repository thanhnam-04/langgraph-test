"""Node 2: Phát hiện Intent (Intent Detection)."""

from src.graph.state import ChatbotState
from src.utils.helper import log_node_execution


def detect_intent(state: ChatbotState) -> ChatbotState:
    log_node_execution("INTENT", "Phát hiện intent...")
    
    question = state.get("cleaned_question", "").lower()
    
    # Intent detection logic (rule-based)
    intent = "other"
    
    greeting_keywords = ["xin chào", "chào", "hello", "hi", "hey"]
    question_keywords = ["gì", "sao", "như thế nào", "hỏi", "tại sao", "khi nào", "ở đâu", "ai", "what", "how", "why", "when", "where", "who"]
    help_keywords = ["giúp", "help", "hướng dẫn", "hỗ trợ", "support"]
    farewell_keywords = ["tạm biệt", "bye", "goodbye", "see you"]
    
    if any(keyword in question for keyword in greeting_keywords):
        intent = "greeting"
    elif any(keyword in question for keyword in question_keywords):
        intent = "question"
    elif any(keyword in question for keyword in help_keywords):
        intent = "help"
    elif any(keyword in question for keyword in farewell_keywords):
        intent = "farewell"
    
    state["intent"] = intent
    
    log_node_execution("INTENT", f"✓ Intent phát hiện: {intent.upper()}")
    
    return state
