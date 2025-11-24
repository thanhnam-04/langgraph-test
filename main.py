"""Main entry point for the chatbot application."""

import os
from dotenv import load_dotenv
from src.graph.builder import create_chatbot_graph
from src.graph.state import ChatbotState
from src.utils.helper import log_node_execution

# Load environment variables
load_dotenv()


def run_chatbot(question: str):
    """
    Chạy chatbot với một câu hỏi.
    
    Args:
        question: Câu hỏi từ user
    """
    print("\n" + "=" * 62)
    print("🤖 CHATBOT LANGGRAPH - MULTI-STEP PIPELINE")
    print("=" * 62)
    
    # Initialize the graph
    log_node_execution("MAIN", "Khởi tạo graph...")
    graph = create_chatbot_graph()
    
    # Define initial state
    initial_state: ChatbotState = {
        "raw_question": question,
        "cleaned_question": None,
        "intent": None,
        "llm_response": None,
        "final_answer": None,
        "error": None,
        "needs_retry": False,
        "retry_count": 0
    }
    
    log_node_execution("MAIN", f"Câu hỏi: '{question}'")
    print()
    
    try:
        # Execute the graph
        final_state = graph.invoke(initial_state)
        
        # Display final answer
        print("\n" + final_state.get("final_answer", "Không có câu trả lời"))
        
        return final_state
        
    except Exception as e:
        log_node_execution("ERROR", f"Lỗi: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        raise


def interactive_mode():
    """Chế độ chat tương tác."""
    print("\n" + "=" * 62)
    print("🤖 CHATBOT INTERACTIVE MODE")
    print("=" * 62)
    print("Gõ 'exit', 'quit' hoặc 'bye' để thoát\n")
    
    graph = create_chatbot_graph()
    
    while True:
        try:
            question = input("\n👤 Bạn: ").strip()
            
            if not question:
                continue
                
            if question.lower() in ['exit', 'quit', 'bye', 'thoát']:
                print("\n👋 Tạm biệt! Hẹn gặp lại!")
                break
            
            # Run chatbot
            initial_state: ChatbotState = {
                "raw_question": question,
                "cleaned_question": None,
                "intent": None,
                "llm_response": None,
                "final_answer": None,
                "error": None,
                "needs_retry": False,
                "retry_count": 0
            }
            
            final_state = graph.invoke(initial_state)
            print("\n" + final_state.get("final_answer", "Không có câu trả lời"))
            
        except KeyboardInterrupt:
            print("\n\n👋 Tạm biệt! Hẹn gặp lại!")
            break
        except Exception as e:
            print(f"\n❌ Lỗi: {str(e)}")


def main():
    """Main function - Chạy trực tiếp interactive mode."""
    interactive_mode()


if __name__ == "__main__":
    main()
