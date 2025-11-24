"""Test which Gemini models are available with your API key"""
import os
from dotenv import load_dotenv

load_dotenv()

def list_available_models():
    """List all available Gemini models"""
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ Không có GOOGLE_API_KEY")
        return
    
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        
        print("📋 Available Gemini Models:\n")
        
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"✅ {model.name}")
                print(f"   Display Name: {model.display_name}")
                print(f"   Description: {model.description[:100]}...")
                print()
        
        # Test with first available model
        print("\n🧪 Testing first available model...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say hello in Vietnamese")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    list_available_models()
