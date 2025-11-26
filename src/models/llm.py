"""Gemini LLM model initialization and configuration."""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_gemini_model():
    """
    Khởi tạo và trả về Gemini model đã được cấu hình.
    
    Returns:
        genai.GenerativeModel hoặc None nếu không có API key
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("⚠️ Warning: GOOGLE_API_KEY not found in environment variables")
        return None
    
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Get model name from env or use default
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        
        # Create and return model instance
        model = genai.GenerativeModel(model_name)
        
        return model
        
    except Exception as e:
        print(f"⚠️ Error configuring Gemini model: {e}")
        return None
