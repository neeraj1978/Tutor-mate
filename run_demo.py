import os
from dotenv import load_dotenv
load_dotenv()

import json
import asyncio
from agents.ingest_agent import IngestAgent
from agents.diagnostic_agent import DiagnosticAgent
from agents.practice_agent import PracticeAgent
from agents.explanation_agent import ExplanationAgent
from agents.quiz_runner import QuizRunner
from agents.progress_tracker import ProgressTracker
from agents.scheduler_agent import SchedulerAgent
from agents.teacher_summary_agent import TeacherSummaryAgent
from tools.memory_bank import MemoryBank

def main():
    print("🚀 Starting TutorMate Demo...")
    
    # 1. Setup
    ingest = IngestAgent()
    diagnostic = DiagnosticAgent()
    practice = PracticeAgent()
    explanation = ExplanationAgent()
    quiz_runner = QuizRunner()
    tracker = ProgressTracker()
    scheduler = SchedulerAgent()
    summary_agent = TeacherSummaryAgent()
    
    # Initialize Memory
    memory = MemoryBank()
    memory.add_student("s001", "Alex Student", 8)
    
    # 2. Ingest Data
    print("\n📥 Ingesting Quiz and Responses...")
    quiz_data = ingest.load_quiz("data/quizzes.json")
    responses_data = ingest.load_quiz("data/samples/student_responses.json") # Reusing load_quiz for json loading
    
    normalized_data = ingest.normalize_responses(responses_data, quiz_data)
    print("✅ Data Normalized.")
    
    # 3. Diagnose
    print("\n🩺 Diagnosing Weak Concepts...")
    diagnosis = diagnostic.diagnose(normalized_data)
    print(f"Diagnosis Result: {json.dumps(diagnosis, indent=2)}")
    
    weak_concepts = diagnosis.get("weak_concepts", [])
    if not weak_concepts:
        print("🎉 No weak concepts found! Great job.")
        # For demo purposes, let's force a weak concept if none found or API failed
        if "error" in diagnosis:
             weak_concepts = [{"concept": "Linear Functions", "confidence": 0.8, "reason": "Simulated error fallback"}]
    
    # 4. Explain
    print("\n💡 Generating Explanations...")
    explanations = explanation.generate_explanations(weak_concepts)
    print(f"Explanations: {json.dumps(explanations, indent=2)}")
    
    # 5. Generate Practice
    print("\n📝 Generating Practice Set...")
    practice_set = practice.generate_practice(weak_concepts)
    print(f"Practice Set: {json.dumps(practice_set, indent=2)}")
    
    # 6. Simulate Practice Session (Quiz Runner)
    print("\n🏃 Running Practice Session (Simulation)...")
    # Simulating student answers for the generated practice
    simulated_answers = {}
    if "practice_set" in practice_set:
        for concept_group in practice_set["practice_set"]:
            for q in concept_group.get("questions", []):
                # Simulate getting it right 50% of the time for demo
                simulated_answers[q["question"]] = q["answer"] # Perfect score for demo simplicity
    
    grading_results = quiz_runner.grade_quiz(practice_set, simulated_answers)
    print(f"Grading Results: {json.dumps(grading_results, indent=2)}")
    
    # 7. Track Progress
    print("\n📈 Tracking Progress...")
    tracker.update_progress("s001", grading_results)
    current_status = tracker.get_student_status("s001")
    print(f"Current Student Status: {current_status}")
    
    # 8. Schedule Next
    print("\n📅 Scheduling Next Session...")
    schedule = scheduler.schedule_next_session(current_status)
    print(f"Next Session: {schedule}")
    
    # 9. Teacher Summary
    print("\n🍎 Generating Teacher Report...")
    report = summary_agent.generate_report("s001", current_status)
    print("\n--- TEACHER REPORT ---\n")
    print(report)
    print("\n----------------------")
    

if __name__ == "__main__":
    main()
