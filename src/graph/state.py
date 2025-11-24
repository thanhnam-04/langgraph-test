"""State definition for chatbot workflow."""

from typing_extensions import TypedDict
from typing import Optional


class ChatbotState(TypedDict):
    """
    State schema for the chatbot workflow.
    
    Attributes:
        raw_question: Câu hỏi gốc từ user
        cleaned_question: Câu hỏi đã được làm sạch
        intent: Intent đã được phát hiện (greeting, question, help, other)
        llm_response: Câu trả lời từ LLM
        final_answer: Câu trả lời cuối cùng đã được format
        error: Lỗi nếu có
        needs_retry: Cờ đánh dấu cần retry
        retry_count: Số lần đã retry
    """
    raw_question: str
    cleaned_question: Optional[str]
    intent: Optional[str]
    llm_response: Optional[str]
    final_answer: Optional[str]
    error: Optional[str]
    needs_retry: Optional[bool]
    retry_count: Optional[int]
