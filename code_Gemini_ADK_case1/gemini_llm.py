import os
import google.generativeai as genai
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv(dotenv_path=".env")

class GeminiLlm:
    """
    Wrapper for google-generativeai v0.8.5 (v1beta API)
    Works with models like 'models/gemini-2.0-flash'
    """
    def __init__(self, model_name: str = "models/gemini-2.0-flash", api_key: str = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Missing Gemini API key. Set GOOGLE_API_KEY in .env or pass directly.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate(self, prompt: str) -> str:
        """Generate text from Gemini model."""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"[GeminiLlm Error] {e}"