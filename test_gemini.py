"""Test Gemini API connection"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_gemini():
    """Test different Gemini models"""
    api_key = os.getenv("GOOGLE_API_KEY")
    print(f"API Key: {api_key[:20]}..." if api_key else "No API key")
    
    if not api_key:
        print("❌ Không có GOOGLE_API_KEY")
        return
    
    models_to_test = [
        "gemini-pro",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
    ]
    
    for model_name in models_to_test:
        print(f"\n🧪 Testing {model_name}...")
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                temperature=0.7,
                google_api_key=api_key
            )
            
            response = llm.invoke("Say 'Hello' in one word")
            print(f"✅ {model_name} works!")
            print(f"   Response: {response.content}")
            break  # Nếu thành công thì dừng
            
        except Exception as e:
            print(f"❌ {model_name} failed: {str(e)[:100]}")
    
if __name__ == "__main__":
    test_gemini()
