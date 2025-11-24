# 🤖 Chatbot LangGraph - Multi-Step Pipeline

Chatbot thông minh sử dụng LangGraph với pipeline xử lý nhiều bước.

## 🎯 Mục tiêu học tập

- ✅ **State Management**: Quản lý state qua các nodes
- ✅ **Nodes**: Tạo và kết nối các processing nodes
- ✅ **Routing**: Điều hướng luồng xử lý
- ✅ **Graph Building**: Xây dựng workflow graph

## 🏗️ Kiến trúc Pipeline

```
START → Node 1 → Node 2 → Node 3 → Node 4 → END
        ↓        ↓        ↓        ↓
    Clean    Detect   Generate  Format
   Question   Intent    LLM     Response
```

### Chi tiết các Node:

1. **Node 1 - Clean Question** 🧹
   - Loại bỏ khoảng trắng thừa
   - Chuẩn hóa dấu câu
   - Loại bỏ ký tự đặc biệt

2. **Node 2 - Detect Intent** 🎯
   - Phát hiện intent: greeting, question, help, farewell, other
   - Sử dụng rule-based matching

3. **Node 3 - Generate LLM Response** 🤖
   - Gọi OpenAI/Anthropic API (nếu có)
   - Fallback về rule-based response

4. **Node 4 - Format Response** ✨
   - Format đẹp với metadata
   - Thêm timestamp và intent info

## 📁 Cấu trúc Project

```
.
├── src/
│   ├── graph/
│   │   ├── builder.py      # Xây dựng LangGraph workflow
│   │   └── state.py        # ChatbotState definition
│   ├── nodes/
│   │   ├── node1.py        # Clean question node
│   │   ├── node2.py        # Intent detection node
│   │   ├── node3.py        # LLM response node
│   │   └── node4.py        # Format response node
│   └── utils/
│       └── helper.py       # Helper functions & LLM calls
├── main.py                 # Entry point với demo & interactive mode
├── .env.example           # Environment variables template
└── pyproject.toml         # Dependencies
```

## 🚀 Cài đặt

### 1. Clone và cài dependencies

```bash
# Install uv nếu chưa có
pip install uv

# Sync dependencies
uv sync
```

### 2. Cấu hình API Key (Optional)

```bash
# Copy file .env.example
cp .env.example .env

# Thêm API key vào .env
# OPENAI_API_KEY=sk-...
# hoặc
# ANTHROPIC_API_KEY=sk-ant-...
```

**Lưu ý**: Nếu không có API key, chatbot vẫn hoạt động với rule-based responses!

## 💻 Sử dụng

### Demo Mode (Mặc định)

```bash
uv run main.py
```

Chạy với 3 câu hỏi mẫu, sau đó hỏi có muốn vào interactive mode.

### Interactive Mode

```bash
# Trong Python
python main.py
# Chọn 'y' khi được hỏi

# Hoặc import và gọi trực tiếp
from main import interactive_mode
interactive_mode()
```

### Single Question

```python
from main import run_chatbot

run_chatbot("LangGraph là gì?")
```

## 📝 Ví dụ

```
👤 Bạn: Xin chào!

[12:30:40] [CLEAN   ] Làm sạch câu hỏi...
[12:30:40] [CLEAN   ] ✓ Câu hỏi gốc: 'Xin chào!'
[12:30:40] [CLEAN   ] ✓ Đã làm sạch: 'Xin chào!'
[12:30:40] [INTENT  ] Phát hiện intent...
[12:30:40] [INTENT  ] ✓ Intent phát hiện: GREETING
[12:30:40] [LLM     ] Tạo câu trả lời...
[12:30:40] [LLM     ] ℹ Không có API key, dùng rule-based response
[12:30:40] [FORMAT  ] Format câu trả lời...
[12:30:40] [FORMAT  ] ✓ Đã format câu trả lời

╔══════════════════════════════════════════════════════════╗
║ 🤖 CHATBOT RESPONSE                                      ║
╠══════════════════════════════════════════════════════════╣
║ Intent: GREETING                                         ║
║ Time: 12:30:40                                           ║
╠══════════════════════════════════════════════════════════╣

Xin chào! Tôi là chatbot AI. Tôi có thể giúp gì cho bạn hôm nay?

╚══════════════════════════════════════════════════════════╝
```

## 🔧 Tùy chỉnh

### Thêm Intent mới

Sửa file `src/nodes/node2.py`:

```python
# Thêm keywords
custom_keywords = ["keyword1", "keyword2"]
if any(keyword in question for keyword in custom_keywords):
    intent = "custom_intent"
```

### Thay đổi LLM Model

Sửa file `src/utils/helper.py`:

```python
llm = ChatOpenAI(model="gpt-4", temperature=0.7)  # Đổi model
```

### Thêm Node mới

1. Tạo file node mới trong `src/nodes/`
2. Import và thêm vào `builder.py`
3. Kết nối edges

## 📚 Học thêm

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Python Docs](https://python.langchain.com/)

## 🎓 Kiến thức đạt được

✅ **State Management**: Hiểu cách state flow qua nodes  
✅ **Node Design**: Thiết kế nodes với single responsibility  
✅ **Graph Building**: Xây dựng và compile StateGraph  
✅ **Routing**: Kết nối nodes với edges  
✅ **LLM Integration**: Tích hợp OpenAI/Anthropic APIs  
✅ **Error Handling**: Xử lý lỗi và fallback logic
