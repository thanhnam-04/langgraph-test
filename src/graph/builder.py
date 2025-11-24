"""Graph builder module for constructing the chatbot workflow."""

from langgraph.graph import StateGraph, START, END

from src.graph.state import ChatbotState
from src.nodes.node1 import clean_question
from src.nodes.node2 import detect_intent
from src.nodes.node3 import generate_llm_response
from src.nodes.node4 import validate_response
from src.nodes.node5 import retry_generate_response
from src.nodes.node6 import format_response
from src.utils.helper import log_node_execution


def should_retry(state: ChatbotState) -> str:
    """
    Routing function: Quyết định có cần retry hay không.
    
    Returns:
        "retry" - Quay lại node retry_generate
        "continue" - Tiếp tục node format
    """
    needs_retry = state.get("needs_retry", False)
    retry_count = state.get("retry_count", 0)
    MAX_RETRIES = 2  # Tối đa retry 2 lần
    
    if needs_retry and retry_count < MAX_RETRIES:
        log_node_execution("ROUTER", f"→ RETRY (lần {retry_count}/{MAX_RETRIES})")
        return "retry"
    else:
        if retry_count >= MAX_RETRIES:
            log_node_execution("ROUTER", "→ CONTINUE (đã hết retry)")
        else:
            log_node_execution("ROUTER", "→ CONTINUE (response OK)")
        return "continue"


def create_chatbot_graph():
    """
    Tạo LangGraph workflow cho chatbot với LOOP (vòng lặp).
    
    Flow:
    START → node1 → node2 → node3 → node4 → router
                                      ↑         ↓
                                    node5 ←─ retry
                                      ↓
                                    continue
                                      ↓
                                    node6 → END
    
    Returns:
        Compiled graph ready for execution
    """
    # Initialize the graph with ChatbotState
    workflow = StateGraph(ChatbotState)
    
    # Add nodes to the graph
    workflow.add_node("clean_question", clean_question)
    workflow.add_node("detect_intent", detect_intent)
    workflow.add_node("generate_llm_response", generate_llm_response)
    workflow.add_node("validate_response", validate_response)
    workflow.add_node("retry_generate", retry_generate_response)
    workflow.add_node("format_response", format_response)
    
    # Define the flow/edges
    workflow.add_edge(START, "clean_question")
    workflow.add_edge("clean_question", "detect_intent")
    workflow.add_edge("detect_intent", "generate_llm_response")
    workflow.add_edge("generate_llm_response", "validate_response")
    
    # CONDITIONAL ROUTING - Tạo vòng lặp
    workflow.add_conditional_edges(
        "validate_response",  # Từ node này
        should_retry,         # Routing function (định nghĩa ở trên)
        {
            "retry": "retry_generate",      # Nếu cần retry → quay lại
            "continue": "format_response"   # Nếu OK → tiếp tục
        }
    )
    
    # Retry xong → quay lại validate (TẠO VÒNG LẶP)
    workflow.add_edge("retry_generate", "validate_response")
    
    # Format xong → END
    workflow.add_edge("format_response", END)
    
    # Compile and return the graph
    return workflow.compile()
