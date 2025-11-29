import json
import os
from typing import Dict, Any

class IngestAgent:
    def __init__(self):
        pass

    def load_quiz(self, file_path: str) -> Dict[str, Any]:
        """
        Loads a quiz JSON file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Quiz file not found: {file_path}")
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data

    def normalize_responses(self, student_responses: Dict[str, Any], quiz_key: Dict[str, Any]) -> Dict[str, Any]:
        """
        Combines student responses with the answer key for diagnosis.
        """
        normalized = {
            "student_id": student_responses.get("student_id"),
            "quiz_id": quiz_key.get("quiz_id"),
            "questions": []
        }

        # Create a map of question_id to key data
        key_map = {q["id"]: q for q in quiz_key.get("questions", [])}

        for resp in student_responses.get("responses", []):
            q_id = resp.get("question_id")
            if q_id in key_map:
                q_data = key_map[q_id]
                normalized["questions"].append({
                    "id": q_id,
                    "question_text": q_data.get("text"),
                    "student_answer": resp.get("answer"),
                    "correct_answer": q_data.get("correct_answer"),
                    "concepts": q_data.get("concepts", [])
                })
        
        return normalized
