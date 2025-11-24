"""Node 3: Gọi LLM để trả lời (LLM Response)."""

import os
from src.graph.state import ChatbotState
from src.utils.helper import log_node_execution


def generate_llm_response(state: ChatbotState) -> ChatbotState:
    """
    Node 3: Gọi LLM để sinh câu trả lời.
    
    Sử dụng Google Gemini API hoặc rule-based response nếu không có API key.
    
    Args:
        state: Current chatbot state
        
    Returns:
        Updated state with LLM response
    """
    log_node_execution("LLM", "Tạo câu trả lời...")
    
    question = state.get("cleaned_question", "")
    intent = state.get("intent", "other")
    
    # Check if API key exists
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if api_key:
        # Use Gemini API
        try:
            from src.utils.helper import call_llm
            response = call_llm(question, intent)
            state["llm_response"] = response
            model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
            log_node_execution("LLM", f"✓ Sử dụng Gemini API ({model})")
        except Exception as e:
            log_node_execution("LLM", f"⚠ Gemini API lỗi: {str(e)}, dùng rule-based")
            state["llm_response"] = generate_rule_based_response(question, intent)
    else:
        # Use rule-based response
        log_node_execution("LLM", "ℹ Không có GOOGLE_API_KEY, dùng rule-based response")
        state["llm_response"] = generate_rule_based_response(question, intent)
    
    log_node_execution("LLM", f"✓ Câu trả lời: {state['llm_response'][:100]}...")
    
    return state


def generate_rule_based_response(question: str, intent: str) -> str:
    """Generate rule-based response based on intent."""
    
    responses = {
        "greeting": "Xin chào! Tôi là chatbot AI. Tôi có thể giúp gì cho bạn hôm nay?",
        "help": "Tôi có thể giúp bạn:\n- Trả lời các câu hỏi\n- Cung cấp thông tin\n- Hỗ trợ giải đáp thắc mắc\nHãy đặt câu hỏi cho tôi!",
        "farewell": "Tạm biệt! Hẹn gặp lại bạn!",
        "question": f"Đây là câu trả lời cho câu hỏi của bạn về: '{question}'. Đây là phiên bản demo, để có câu trả lời chính xác hơn, vui lòng cấu hình GOOGLE_API_KEY trong file .env",
        "other": "Tôi chưa hiểu rõ câu hỏi của bạn. Bạn có thể diễn đạt lại được không?"
    }
    
    return responses.get(intent, responses["other"])
