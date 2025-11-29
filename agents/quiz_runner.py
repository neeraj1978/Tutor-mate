from typing import Dict, Any, List
try:
    from tools.math_solver import MathSolver
except ImportError:
    # Fallback for when running from a different context
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from tools.math_solver import MathSolver

class QuizRunner:
    def __init__(self):
        self.math_solver = MathSolver()

    def grade_quiz(self, practice_set: Dict[str, Any], student_answers: Dict[str, str]) -> Dict[str, Any]:
        """
        Grades the practice set.
        """
        results = {
            "score": 0,
            "total": 0,
            "details": []
        }

        for concept_group in practice_set.get("practice_set", []):
            for q in concept_group.get("questions", []):
                q_text = q.get("question")
                correct_ans = q.get("answer")
                student_ans = student_answers.get(q_text, "")
                
                is_correct = self.math_solver.validate_answer(student_ans, correct_ans)
                
                results["total"] += 1
                if is_correct:
                    results["score"] += 1
                
                results["details"].append({
                    "question": q_text,
                    "student_answer": student_ans,
                    "correct_answer": correct_ans,
                    "is_correct": is_correct,
                    "concept": concept_group.get("concept")
                })
        
        return results
