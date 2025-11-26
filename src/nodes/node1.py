"""Node 1: Làm sạch câu hỏi (Clean Question)."""

import re
from src.graph.state import ChatbotState
from src.utils.helper import log_node_execution


def clean_question(state: ChatbotState) -> ChatbotState:

    log_node_execution("CLEAN", "Làm sạch câu hỏi...")
    
    raw_question = state.get("raw_question", "")
    
    # Loại bỏ khoảng trắng thừa
    cleaned = re.sub(r'\s+', ' ', raw_question).strip()
    
    # Loại bỏ ký tự đặc biệt (giữ lại chữ, số, dấu câu cơ bản)
    cleaned = re.sub(r'[^\w\s\?\!\.\,\-\:àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', '', cleaned, flags=re.IGNORECASE)
    
    # Chuẩn hóa dấu câu
    cleaned = re.sub(r'\s+([?.!,])', r'\1', cleaned)
    
    state["cleaned_question"] = cleaned
    
    log_node_execution("CLEAN", f"✓ Câu hỏi gốc: '{raw_question}'")
    log_node_execution("CLEAN", f"✓ Đã làm sạch: '{cleaned}'")
    
    return state
