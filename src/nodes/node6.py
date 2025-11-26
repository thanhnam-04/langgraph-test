"""Node 4: Format câu trả lời (Format Response)."""

from datetime import datetime
from src.graph.state import ChatbotState
from src.utils.helper import log_node_execution


def format_response(state: ChatbotState) -> ChatbotState:
    
    log_node_execution("FORMAT", "Format câu trả lời...")
    
    llm_response = state.get("llm_response", "")
    intent = state.get("intent", "other")
    
    # Format response with metadata
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    formatted = f"""
╔══════════════════════════════════════════════════════════╗
║ 🤖 CHATBOT RESPONSE                                      ║
╠══════════════════════════════════════════════════════════╣
║ Intent: {intent.upper():<48} ║
║ Time: {timestamp:<50} ║
╠══════════════════════════════════════════════════════════╣

{llm_response}

╚══════════════════════════════════════════════════════════╝
    """.strip()
    
    state["final_answer"] = formatted
    
    log_node_execution("FORMAT", "✓ Đã format câu trả lời")
    
    return state
