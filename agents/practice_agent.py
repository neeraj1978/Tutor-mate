import os
import json
try:
    import google.generativeai as genai
except ImportError:
    genai = None
from typing import List, Dict, Any

class PracticeAgent:
    def __init__(self, model_name: str = "models/gemini-2.5-flash"):
        self.model_name = model_name
        self._setup_genai()
        self.prompt_template = self._load_prompt()

    def _setup_genai(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key and genai:
            genai.configure(api_key=api_key)

    def _load_prompt(self) -> str:
        try:
            with open("prompts/practice.txt", "r") as f:
                return f.read()
        except FileNotFoundError:
            return "Generate practice questions for: {concepts}"

    def generate_practice(self, weak_concepts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generates practice questions for the given weak concepts.
        """
        if not os.getenv("GOOGLE_API_KEY") or genai is None:
            return {"error": "Missing API Key or genai module", "practice_set": []}

        model = genai.GenerativeModel(self.model_name)
        
        concepts_str = ", ".join([c["concept"] for c in weak_concepts])
        prompt = self.prompt_template.replace("{concepts}", concepts_str)
        
        try:
            response = model.generate_content(prompt)
            return self._parse_response(response.text)
        except Exception as e:
            print(f"Error in practice generation: {e}")
            return {"error": str(e)}

    def _parse_response(self, text: str) -> Dict[str, Any]:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"raw_text": text}
