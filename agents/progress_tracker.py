from typing import Dict, Any, List
try:
    from tools.memory_bank import MemoryBank
except ImportError:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from tools.memory_bank import MemoryBank

class ProgressTracker:
    def __init__(self):
        self.memory = MemoryBank()

    def update_progress(self, student_id: str, grading_results: Dict[str, Any]):
        """
        Updates the memory bank with the results of the practice session.
        """
        for detail in grading_results.get("details", []):
            concept = detail.get("concept")
            is_correct = detail.get("is_correct")
            
            # Simple logic: +0.1 for correct, -0.05 for incorrect
            delta = 0.1 if is_correct else -0.05
            mistake = None if is_correct else f"Failed question: {detail.get('question')}"
            
            self.memory.update_concept_mastery(student_id, concept, delta, mistake)

    def get_student_status(self, student_id: str) -> List[Dict[str, Any]]:
        return self.memory.get_student_mastery(student_id)
