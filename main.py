import os
from dotenv import load_dotenv
from src.graph.builder import create_chatbot_graph
from src.graph.state import ChatbotState
from src.utils.helper import log_node_execution

# Load environment variables
load_dotenv()


def chat_mode():
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
    chat_mode()


if __name__ == "__main__":
    main()
