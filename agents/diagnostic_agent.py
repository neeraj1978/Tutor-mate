import os
import json
try:
    import google.generativeai as genai
except ImportError:
    genai = None
from typing import Dict, Any

class DiagnosticAgent:
    def __init__(self, model_name: str = "models/gemini-2.5-flash"):
        self.model_name = model_name
        self._setup_genai()
        self.prompt_template = self._load_prompt()

    def _setup_genai(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("Warning: GOOGLE_API_KEY not set. Gemini calls will fail.")
        elif genai:
            genai.configure(api_key=api_key)
        else:
            print("Warning: google.generativeai module not found.")

    def _load_prompt(self) -> str:
        try:
            with open("prompts/diagnostic.txt", "r") as f:
                return f.read()
        except FileNotFoundError:
            return "Analyze the following student responses and identify weak concepts: {data}"

    def diagnose(self, normalized_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Uses Gemini to analyze student performance.
        """
        if not os.getenv("GOOGLE_API_KEY") or genai is None:
             return {"error": "Missing API Key or genai module", "diagnosis": "Simulation: Weakness in Algebra detected."}

        model = genai.GenerativeModel(self.model_name)
        
        data_str = json.dumps(normalized_data, indent=2)
        prompt = self.prompt_template.replace("{data}", data_str)
        
        try:
            response = model.generate_content(prompt)
            # Expecting JSON output from the model, or we parse it.
            # For robustness, we'll ask the model to output JSON.
            return self._parse_response(response.text)
        except Exception as e:
            print(f"Error in diagnosis: {e}")
            return {"error": str(e)}

    def _parse_response(self, text: str) -> Dict[str, Any]:
        # Simple cleanup to extract JSON if wrapped in markdown
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"raw_text": text}
