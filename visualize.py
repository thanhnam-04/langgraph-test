"""Visualize chatbot workflow graph."""

from src.graph.builder import create_chatbot_graph


def draw_graph():
    """Vẽ graph tự động từ LangGraph."""
    print("\n" + "=" * 65)
    print("🎨 CHATBOT WORKFLOW VISUALIZATION")
    print("=" * 65)
    
    graph = create_chatbot_graph()
    
    try:
        # LangGraph có phương thức get_graph() để lấy cấu trúc
        from langgraph.graph import START, END
        
        print("\n📊 Graph được vẽ tự động từ LangGraph:\n")
        
        # In cấu trúc graph dưới dạng text
        ascii_graph = graph.get_graph().draw_ascii()
        print(ascii_graph)
        
    except AttributeError:
        print("\n⚠️ Phương thức draw_ascii() không có sẵn.")
        print("Thử phương thức khác...\n")
        
        try:
            # Thử xuất Mermaid
            mermaid = graph.get_graph().draw_mermaid()
            print("📊 Mermaid Diagram:")
            print("\nCopy đoạn code sau vào https://mermaid.live:\n")
            print(mermaid)
        except Exception as e:
            print(f"❌ Không thể vẽ graph tự động: {e}")
            print("\n💡 Cài thêm thư viện: uv add grandalf")
    
    except Exception as e:
        print(f"❌ Lỗi: {e}")


def print_graph_structure():
    """In cấu trúc graph."""
    graph = create_chatbot_graph()
    
    print("\n" + "=" * 65)
    print("📋 GRAPH STRUCTURE")
    print("=" * 65)
    
    try:
        graph_data = graph.get_graph()
        
        print(f"\n✅ Graph type: {type(graph).__name__}")
        print(f"\n🔍 Nodes: {len(graph_data.nodes)}")
        for node in graph_data.nodes:
            if node not in ['__start__', '__end__']:
                print(f"   - {node}")
        
        print(f"\n🔗 Edges: {len(graph_data.edges)}")
        for edge in graph_data.edges:
            print(f"   - {edge}")
            
    except Exception as e:
        print(f"❌ Không thể lấy thông tin graph: {e}")


if __name__ == "__main__":
    draw_graph()
    print("\n" + "=" * 65)
    print_graph_structure()
    """Vẽ graph dạng ASCII art."""
    print("""
┌─────────────────────────────────────────────────────────────────┐
│              CHATBOT WORKFLOW - LANGGRAPH                        │
└─────────────────────────────────────────────────────────────────┘

        👤 USER INPUT
             │
             ▼
        ┌─────────┐
        │  START  │
        └────┬────┘
             │
             ▼
    ┌────────────────┐
    │  NODE 1        │  clean_question
    │  Làm sạch      │  Input: raw_question
    │                │  Output: cleaned_question
    └────────┬───────┘
             │
             ▼
    ┌────────────────┐
    │  NODE 2        │  detect_intent
    │  Phát hiện     │  Input: cleaned_question
    │  Intent        │  Output: intent
    └────────┬───────┘
             │
             ▼
    ┌────────────────┐
    │  NODE 3        │  generate_llm_response
    │  Gọi Gemini    │  Input: cleaned_question, intent
    │  API           │  Output: llm_response
    └────────┬───────┘
             │
             ▼
    ┌────────────────────────────────┐
    │  NODE 4                        │  validate_response
    │  Kiểm tra chất lượng           │  Input: llm_response
    │  (>20 từ?)                     │  Output: needs_retry, retry_count
    └──────────┬─────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │  ROUTING FUNCTION    │  should_retry()
    │  Quyết định đường đi │  
    └──┬──────────────┬────┘
       │              │
retry  │              │ continue
       │              │
┌──────▼───────┐     │
│  NODE 5      │     │  retry_generate_response
│  Retry với   │     │  Input: cleaned_question, intent
│  prompt tốt  │     │  Output: llm_response (mới)
│  hơn (>50 từ)│     │
└──────┬───────┘     │
       │             │
       │◄────────────┘
       │  (VÒNG LẶP: max 2 lần)
       │
       └─────────────────────────┐
                                 │
                                 ▼
                        ┌────────────────┐
                        │  NODE 6        │  format_response
                        │  Format box    │  Input: llm_response, intent
                        │  với Unicode   │  Output: final_answer
                        └────────┬───────┘
                                 │
                                 ▼
                            ┌─────────┐
                            │   END   │
                            └────┬────┘
                                 │
                                 ▼
                    📤 OUTPUT: Câu trả lời đẹp
                    
┌─────────────────────────────────────────────────────────────────┐
│  THỐNG KÊ:                                                      │
│  - Tổng số nodes: 6                                             │
│  - Normal edges: 6                                              │
│  - Conditional edges: 1 (validate → router → retry/continue)    │
│  - Vòng lặp: node5 → node4 (retry loop)                        │
└─────────────────────────────────────────────────────────────────┘
""")


def draw_mermaid_graph():
    """Vẽ graph dạng Mermaid (copy vào https://mermaid.live)."""
    mermaid_code = """
```mermaid
graph TD
    Start([START]) --> Node1[NODE 1<br/>clean_question]
    Node1 --> Node2[NODE 2<br/>detect_intent]
    Node2 --> Node3[NODE 3<br/>generate_llm_response]
    Node3 --> Node4[NODE 4<br/>validate_response]
    Node4 --> Router{should_retry?}
    Router -->|retry| Node5[NODE 5<br/>retry_generate_response]
    Router -->|continue| Node6[NODE 6<br/>format_response]
    Node5 --> Node4
    Node6 --> End([END])
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style Router fill:#FFD700
    style Node4 fill:#87CEEB
    style Node5 fill:#FFA07A
```
"""
    print("\n" + "=" * 65)
    print("📊 MERMAID DIAGRAM")
    print("=" * 65)
    print("\nCopy đoạn code sau vào https://mermaid.live để xem graph:")
    print(mermaid_code)


def print_graph_info():
    """In thông tin về graph."""
    print("\n" + "=" * 65)
    print("📋 GRAPH INFORMATION")
    print("=" * 65)
    
    graph = create_chatbot_graph()
    
    print("\n✅ Graph đã được compile thành công!")
    print(f"\n📌 Graph type: {type(graph).__name__}")
    
    # Try to get graph info
    try:
        print("\n🔍 Graph structure:")
        print(f"   - Nodes: 6 (node1, node2, node3, node4, node5, node6)")
        print(f"   - Edges: 6 (5 normal + 1 conditional)")
        print(f"   - Entry point: START → node1")
        print(f"   - Exit point: node6 → END")
        print(f"   - Loop: node5 → node4 (conditional)")
    except Exception as e:
        print(f"   (Không thể lấy thông tin chi tiết: {e})")

if __name__ == "__main__":
    draw_graph()
    print("\n" + "=" * 65)
    print_graph_structure()

