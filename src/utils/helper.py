"""Utility helper functions for the chatbot."""

import os
from datetime import datetime
from typing import Any, Dict


def log_node_execution(node_name: str, message: str) -> None:
    """
    Log node execution information.
    
    Args:
        node_name: Name of the node being executed
        message: Log message
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{node_name:8}] {message}")


def call_llm(question: str, intent: str) -> str:
    """
    Call LLM API to generate response.
    
    Args:
        question: Cleaned question
        intent: Detected intent
        
    Returns:
        LLM response
    """
    google_key = os.getenv("GOOGLE_API_KEY")
    
    if google_key:
        return call_gemini(question, intent)
    else:
        raise Exception("No API key found")


def call_gemini(question: str, intent: str) -> str:
    """
    Call Google Gemini API using google-generativeai SDK directly.
    
    Args:
        question: User question
        intent: Detected intent
        
    Returns:
        Gemini response
    """
    import google.generativeai as genai
    
    # Configure API
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # Get model from env or use default
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    # Create model
    model = genai.GenerativeModel(model_name)
    
    # Create prompt based on intent
    prompts = {
        "greeting": f"Bạn là chatbot thân thiện. Hãy chào hỏi người dùng một cách nhiệt tình và lịch sự.\n\nCâu hỏi: {question}",
        "question": f"Bạn là chatbot hỗ trợ. Hãy trả lời câu hỏi một cách chính xác, ngắn gọn và dễ hiểu.\n\nCâu hỏi: {question}",
        "help": f"Bạn là chatbot hỗ trợ. Hãy giải thích những gì bạn có thể giúp đỡ người dùng.\n\nCâu hỏi: {question}",
        "farewell": f"Bạn là chatbot thân thiện. Hãy chào tạm biệt người dùng một cách ấm áp.\n\nCâu hỏi: {question}",
        "other": f"Bạn là chatbot hữu ích. Hãy trả lời ngắn gọn và thân thiện.\n\nCâu hỏi: {question}"
    }
    
    prompt = prompts.get(intent, prompts["other"])
    
    # Generate response
    response = model.generate_content(prompt)
    return response.text
