"""Node: Validate response - Kiểm tra chất lượng câu trả lời."""

from src.graph.state import ChatbotState
from src.utils.helper import log_node_execution


def validate_response(state: ChatbotState) -> ChatbotState:
    """
    Kiểm tra chất lượng câu trả lời từ LLM.
    
    Nếu câu trả lời quá ngắn → đánh dấu cần retry
    """
    log_node_execution("VALIDATE", "Kiểm tra chất lượng câu trả lời...")
    
    llm_response = state.get("llm_response", "")
    word_count = len(llm_response.split())
    
    # Quy tắc validation
    MIN_WORDS = 20
    
    if word_count < MIN_WORDS:
        log_node_execution("VALIDATE", f"⚠️ Câu trả lời quá ngắn ({word_count} từ). Cần retry!")
        state["needs_retry"] = True
        state["retry_count"] = state.get("retry_count", 0) + 1
    else:
        log_node_execution("VALIDATE", f"✓ Câu trả lời OK ({word_count} từ)")
        state["needs_retry"] = False
    
    return state
