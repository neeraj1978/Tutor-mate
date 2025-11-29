import os
import json
try:
    import google.generativeai as genai
except ImportError:
    genai = None
from typing import List, Dict, Any

class ChatAgent:
    def __init__(self, model_name: str = "models/gemini-2.5-flash"):
        self.model_name = model_name
        self._setup_genai()

    def _setup_genai(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key and genai:
            genai.configure(api_key=api_key)

    def start_session(self, subject: str, difficulty: str = "intermediate", grade_level: str = "College Year 1") -> Dict[str, Any]:
        """
        Starts a new chat session with specified difficulty and grade level.
        """
        difficulty_prompts = {
            "beginner": "Ask simple, foundational questions.",
            "intermediate": "Ask conceptual questions.",
            "advanced": "Ask challenging, advanced questions."
        }
        
        level_prompt = difficulty_prompts.get(difficulty, difficulty_prompts["intermediate"])
        
        prompt = f"""
        You are a friendly and professional tutor named TutorMate.
        
        Context:
        - Subject: {subject}
        - Student Level: {grade_level} (This is CRITICAL. Adjust your tone and complexity to match this exact grade/year.)
        - Difficulty Setting: {difficulty}
        
        Instructions:
        1. {level_prompt}
        2. Ensure the question is appropriate for a student in {grade_level}.
           - For School (Class 1-12): Use simpler language, relatable examples.
           - For College: Use academic terms, practical applications.
        3. Introduce yourself briefly.
        4. Ask the first question.
        
        Output JSON:
        {{
            "message": "Hello! I'm TutorMate...",
            "question": "..."
        }}
        """
        return self._generate(prompt)

    def process_response(self, subject: str, history: List[Dict[str, str]], last_answer: str, difficulty: str = "intermediate", grade_level: str = "College Year 1") -> Dict[str, Any]:
        """
        Evaluates the student's answer and generates the next step.
        """
        history_str = json.dumps(history[-5:]) # Keep context manageable
        
        prompt = f"""
        You are a tutor for {subject}.
        Student Level: {grade_level}
        Difficulty Setting: {difficulty}
        
        Conversation History:
        {history_str}
        
        Student's Last Answer: "{last_answer}"
        
        Task:
        1. Evaluate the answer.
        2. Provide constructive feedback appropriate for a {grade_level} student.
        3. Generate the next question.
           - If the student is struggling, make it easier.
           - If the student is doing well, maintain or slightly increase complexity (within {grade_level} scope).
        4. Identify the concept being tested.
        
        Output JSON:
        {{
            "feedback": "...",
            "next_question": "...",
            "is_correct": true/false,
            "concept": "Concept Name",
            "difficulty": "{difficulty}"
        }}
        """
        return self._generate(prompt)

    def generate_recommendations(self, subject: str, weak_concepts: List[str], difficulty: str) -> Dict[str, Any]:
        """
        Generates specific video recommendations based on weak concepts.
        """
        concepts_str = ", ".join(weak_concepts) if weak_concepts else "general topics"
        
        prompt = f"""
        You are an expert educational counselor.
        Subject: {subject}
        Difficulty: {difficulty}
        Weak Concepts: {concepts_str}
        
        Task:
        Recommend 3 specific, high-quality YouTube video titles or channels that would help a student master these concepts.
        Focus on popular, well-regarded educational channels (e.g., Crash Course, Khan Academy, 3Blue1Brown, organic chemistry tutor, etc.).
        
        Output JSON:
        {{
            "recommendations": [
                {{
                    "title": "Specific Video Title or Topic",
                    "channel": "Channel Name",
                    "query": "Optimized YouTube Search Query"
                }}
            ]
        }}
        """
        return self._generate(prompt)

    def _generate(self, prompt: str) -> Dict[str, Any]:
        if not os.getenv("GOOGLE_API_KEY") or not genai:
            return {
                "message": "Simulation: API Key missing.",
                "question": "Simulation Question?",
                "feedback": "Simulation Feedback",
                "next_question": "Simulation Next Question",
                "is_correct": True,
                "concept": "Simulation",
                "difficulty": "Easy"
            }

        model = genai.GenerativeModel(self.model_name)
        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            return json.loads(text)
        except Exception as e:
            print(f"Error in ChatAgent: {e}")
            return {"error": str(e)}
