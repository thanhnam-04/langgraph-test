"""Node: Retry Generator - Tạo lại câu trả lời chi tiết hơn."""

import os
from src.graph.state import ChatbotState
from src.utils.helper import log_node_execution


def retry_generate_response(state: ChatbotState) -> ChatbotState:
    """
    Gọi lại LLM với prompt yêu cầu chi tiết hơn.
    """
    log_node_execution("RETRY", "Yêu cầu LLM trả lời chi tiết hơn...")
    
    question = state.get("cleaned_question", "")
    intent = state.get("intent", "other")
    retry_count = state.get("retry_count", 1)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            
            model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
            model = genai.GenerativeModel(model_name)
            
            # Prompt yêu cầu chi tiết hơn
            enhanced_prompt = f"""
Bạn là chatbot chuyên nghiệp. Trả lời câu hỏi sau một cách CHI TIẾT, ĐẦY ĐỦ và DỄ HIỂU.

Yêu cầu:
- Tối thiểu 50 từ
- Giải thích rõ ràng
- Có ví dụ minh họa nếu có thể
- Chia thành các đoạn ngắn

Câu hỏi: {question}
            """.strip()
            
            response = model.generate_content(enhanced_prompt)
            state["llm_response"] = response.text
            
            log_node_execution("RETRY", f"✓ Retry lần {retry_count} hoàn thành")
            
        except Exception as e:
            log_node_execution("RETRY", f"⚠️ Lỗi: {str(e)}")
            state["llm_response"] = f"Xin lỗi, đã có lỗi khi retry: {str(e)}"
    else:
        state["llm_response"] = "Cần cấu hình GOOGLE_API_KEY để sử dụng tính năng retry."
    
    return state
