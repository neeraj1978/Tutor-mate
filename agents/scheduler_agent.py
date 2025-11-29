import datetime
from typing import List, Dict, Any

class SchedulerAgent:
    def __init__(self):
        pass

    def schedule_next_session(self, student_status: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Determines what to study next based on mastery scores and time since last practice.
        """
        # Sort by mastery score (ascending) and time since last practice (descending)
        # For simplicity, we just prioritize lowest mastery.
        
        sorted_concepts = sorted(student_status, key=lambda x: x['mastery_score'])
        
        # Pick top 3 weakest concepts
        focus_concepts = [c['concept_id'] for c in sorted_concepts[:3]]
        
        return {
            "next_session_focus": focus_concepts,
            "suggested_time": (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat()
        }
