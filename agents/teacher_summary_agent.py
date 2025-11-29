import os
import json
try:
    import google.generativeai as genai
except ImportError:
    genai = None
from typing import List, Dict, Any

class TeacherSummaryAgent:
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
            with open("prompts/summary.txt", "r") as f:
                return f.read()
        except FileNotFoundError:
            return "Summarize student progress: {data}"

    def generate_report(self, student_id: str, progress_data: List[Dict[str, Any]]) -> str:
        """
        Generates a human-readable report for the teacher.
        """
        if not os.getenv("GOOGLE_API_KEY") or genai is None:
            return "Simulation: Student is improving in Algebra but needs help with Geometry."

        model = genai.GenerativeModel(self.model_name)
        
        data_str = json.dumps(progress_data, indent=2)
        prompt = self.prompt_template.replace("{data}", data_str)
        
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error in summary generation: {e}")
            return f"Error generating report: {e}"
