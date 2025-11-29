import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from fastapi.middleware.cors import CORSMiddleware
import json
import shutil
from datetime import datetime

# Import Agents
from agents.ingest_agent import IngestAgent
from agents.diagnostic_agent import DiagnosticAgent
from agents.practice_agent import PracticeAgent
from agents.explanation_agent import ExplanationAgent
from agents.quiz_runner import QuizRunner
from agents.progress_tracker import ProgressTracker
from agents.scheduler_agent import SchedulerAgent
from agents.teacher_summary_agent import TeacherSummaryAgent
from agents.chat_agent import ChatAgent
from agents.chat_agent import ChatAgent
from agents.game_service import GameService
from tools.memory_bank import MemoryBank
from tools.user_database import UserDatabase

# Load Env
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="TutorMate API", version="1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Agents
ingest = IngestAgent()
diagnostic = DiagnosticAgent()
practice = PracticeAgent()
explanation = ExplanationAgent()
quiz_runner = QuizRunner()
tracker = ProgressTracker()
scheduler = SchedulerAgent()
summary_agent = TeacherSummaryAgent()
chat_agent = ChatAgent()
memory = MemoryBank()
user_db = UserDatabase()
user_db = UserDatabase()
game_service = GameService()

# Data Models
class ChatStartRequest(BaseModel):
    subject: str
    difficulty: str = "intermediate"
    grade_level: str = "College Year 1"

class ChatMessageRequest(BaseModel):
    session_id: str
    message: str
    history: List[Dict[str, str]] = []
    difficulty: str = "intermediate"
    grade_level: str = "College Year 1"
    image: Optional[str] = None # Add image field

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    grade_level: str = "College Year 1"

class LoginRequest(BaseModel):
    email: str
    password: str

class StudentResponse(BaseModel):
    student_id: str
    responses: List[Dict[str, Any]]

class QuizData(BaseModel):
    quiz_id: str
    questions: List[Dict[str, Any]]

# Global state for demo simplicity (in real app, use DB)
CURRENT_DATA = {
    "quiz": None,
    "responses": None,
    "normalized": None,
    "diagnosis": None,
    "weak_concepts": [],
    "practice_set": None
}

@app.get("/")
def read_root():
    return {"message": "TutorMate API is running 🚀"}

# --- Authentication Endpoints ---

@app.post("/auth/register")
def register(request: RegisterRequest):
    """Register a new user"""
    # Validation
    if not request.email.endswith("@gmail.com"):
        raise HTTPException(status_code=400, detail="Only @gmail.com email addresses are allowed.")
    
    if len(request.password) < 5:
        raise HTTPException(status_code=400, detail="Password must be at least 5 characters long.")

    result = user_db.register_user(request.name, request.email, request.password, request.grade_level)
    if result["success"]:
        return {"success": True, "user": result}
    else:
        raise HTTPException(status_code=400, detail=result["error"])

@app.post("/auth/login")
def login(request: LoginRequest):
    """Login user"""
    result = user_db.login_user(request.email, request.password)
    if result["success"]:
        return {"success": True, "user": result["user"]}
    else:
        raise HTTPException(status_code=401, detail=result["error"])

# --- Dashboard Endpoints ---

@app.get("/dashboard/{user_id}")
def get_dashboard(user_id: int):
    """Get dashboard data for a user"""
    try:
        stats = user_db.get_user_stats(user_id)
        sessions = user_db.get_user_sessions(user_id, limit=5)
        
        return {
            "stats": stats,
            "recent_sessions": sessions,
            "has_sessions": len(sessions) > 0
        }
    except Exception as e:
        print(f"Dashboard error: {e}")
        return {
            "stats": {"total_sessions": 0, "average_score": 0, "subjects": []},
            "recent_sessions": [],
            "has_sessions": False
        }

@app.post("/ingest/quiz")
async def ingest_quiz(file: UploadFile = File(...)):
    try:
        content = await file.read()
        data = json.loads(content)
        CURRENT_DATA["quiz"] = data
        return {"status": "success", "message": "Quiz ingested", "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/ingest/responses")
async def ingest_responses(file: UploadFile = File(...)):
    try:
        content = await file.read()
        data = json.loads(content)
        CURRENT_DATA["responses"] = data
        
        if CURRENT_DATA["quiz"]:
            CURRENT_DATA["normalized"] = ingest.normalize_responses(data, CURRENT_DATA["quiz"])
            
        return {"status": "success", "message": "Responses ingested", "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/diagnose")
def run_diagnosis():
    if not CURRENT_DATA["normalized"]:
        raise HTTPException(status_code=400, detail="No normalized data found. Ingest quiz and responses first.")
    
    diagnosis = diagnostic.diagnose(CURRENT_DATA["normalized"])
    CURRENT_DATA["diagnosis"] = diagnosis
    CURRENT_DATA["weak_concepts"] = diagnosis.get("weak_concepts", [])
    
    return diagnosis

@app.get("/explain")
def get_explanations():
    if not CURRENT_DATA["weak_concepts"]:
        return {"explanations": []}
    
    explanations = explanation.generate_explanations(CURRENT_DATA["weak_concepts"])
    return explanations

@app.get("/practice")
def get_practice():
    if not CURRENT_DATA["weak_concepts"]:
        return {"practice_set": []}
    
    practice_set = practice.generate_practice(CURRENT_DATA["weak_concepts"])
    CURRENT_DATA["practice_set"] = practice_set
    return practice_set

@app.post("/submit_practice")
def submit_practice(answers: Dict[str, str]):
    if not CURRENT_DATA["practice_set"]:
        raise HTTPException(status_code=400, detail="No active practice set.")
    
    results = quiz_runner.grade_quiz(CURRENT_DATA["practice_set"], answers)
    
    # Update tracker
    student_id = CURRENT_DATA.get("responses", {}).get("student_id", "unknown")
    tracker.update_progress(student_id, results)
    
    return results

@app.get("/student/{student_id}/summary")
def get_student_summary(student_id: str):
    status = tracker.get_student_status(student_id)
    report = summary_agent.generate_report(student_id, status)
    return {
        "status": status,
        "report": report
    }

# --- Chat Endpoints ---

@app.post("/chat/start")
def start_chat(request: ChatStartRequest):
    response = chat_agent.start_session(request.subject, request.difficulty, request.grade_level)
    # Initialize session tracking if needed
    return response

@app.post("/chat/message")
def chat_message(request: ChatMessageRequest):
    # In a real app, we'd fetch history from DB using session_id
    # Here we trust the client to send relevant history or we just use the last few
    
    response = chat_agent.process_response(
        subject="General", # Ideally passed or stored in session
        history=request.history,
        last_answer=request.message,
        difficulty=request.difficulty,
        grade_level=request.grade_level
    )
    
    # Track progress immediately
    if "is_correct" in response:
        # Update tracker (simplified)
        pass 
        
    return response

@app.get("/game/current")
def get_current_game(user_id: int):
    """Get the current game with 1-hour cooldown"""
    try:
        # Get last attempt
        last_attempt = user_db.get_last_game_attempt(user_id)
        
        cooldown_duration = 3600 # 1 hour
        time_remaining = 0
        played = False
        last_result = None
        
        if last_attempt:
            # Calculate time since last attempt
            # SQLite CURRENT_TIMESTAMP is UTC
            last_time = datetime.strptime(last_attempt["completed_at"], "%Y-%m-%d %H:%M:%S")
            # We assume system time is roughly synced or use utcnow if possible, 
            # but for simplicity with local dev, let's check if the stored time is naive
            
            # Simple check: compare with datetime.utcnow()
            time_since = (datetime.utcnow() - last_time).total_seconds()
            
            # Fallback if time_since is negative (e.g. timezone mismatch), treat as 0
            if time_since < 0:
                time_since = 0
                
            if time_since < cooldown_duration:
                played = True
                time_remaining = int(cooldown_duration - time_since)
                
                # Reconstruct reward
                score = last_attempt["score"]
                reward = "None"
                if score == 100: reward = "Gold"
                elif score >= 66: reward = "Silver"
                elif score >= 33: reward = "Bronze"
                
                last_result = {
                    "correct": score == 100, # Simplified
                    "score": score,
                    "reward": reward,
                    "correct_answer": "See previous result"
                }

        game_data = game_service.get_current_game()
        
        if not played:
            # Use the window's time remaining for the answering phase
            time_remaining = game_data["time_remaining"]
            
        return {
            "played": played,
            "game": game_data["game"],
            "time_remaining": time_remaining,
            "window_id": game_data["window_id"],
            "last_result": last_result
        }
    except Exception as e:
        print(f"Game Error: {e}")
        raise HTTPException(status_code=500, detail="Game service unavailable")

@app.post("/game/submit")
def submit_game(request: dict):
    """Submit an answer for the game"""
    try:
        user_id = request.get("user_id")
        window_id = request.get("window_id")
        answer = request.get("answer")
        
        if not all([user_id, window_id, answer]):
            raise HTTPException(status_code=400, detail="Missing required fields")
            
        # Double check replay
        if user_db.has_played_window(user_id, window_id):
             raise HTTPException(status_code=400, detail="Already played this round")
             
        result = game_service.validate_answer(window_id, answer)
        
        # Record attempt
        user_db.record_game_attempt(user_id, window_id, result["score"])
        
        return result
        
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Game Submit Error: {e}")
        raise HTTPException(status_code=500, detail="Submission failed")

@app.post("/chat/analyze")
def analyze_session(request: dict):
    """
    Generate analysis from chat session
    """
    try:
        session_data = request.get("session_data", {})
        messages = session_data.get("messages", [])
        difficulty = session_data.get("difficulty", "intermediate")
        subject = session_data.get("subject", "General")
        grade_level = session_data.get("grade_level", "College Year 1")
        user_id = request.get("user_id", None)
        
        # Calculate score based on interaction quality (simplified)
        # Calculate score based on correctness
        # We look for AI messages that have the 'is_correct' flag
        ai_responses = [msg for msg in messages if msg.get("role") == "ai" and "is_correct" in msg]
        
        if ai_responses:
            total_questions = len(ai_responses)
            correct_count = 0
            for msg in ai_responses:
                is_correct = msg.get("is_correct")
                if is_correct is True:
                    correct_count += 1
                elif isinstance(is_correct, str) and is_correct.lower() == "true":
                    correct_count += 1
            print(f"DEBUG: Calculated score - Correct: {correct_count}/{total_questions}")
        else:
            # Fallback for sessions without flags (should not happen with new frontend)
            # Count user messages as attempts
            user_messages = [msg for msg in messages if msg.get("role") == "user"]
            total_questions = len(user_messages)
            correct_count = 0
            # Try to infer correctness from text if needed, or just default to 0 to be safe
            # But requirement says: "Do not show a high score unless the model has validated the answer as correct."
            # So we should be strict.
            for msg in messages:
                if msg.get("role") == "ai":
                    content = msg.get("content", "").lower()
                    # Strict heuristic: must contain "correct" and NOT "incorrect"
                    if "correct" in content and "incorrect" not in content:
                        correct_count += 1
        
        if total_questions == 0:
            overall_score = 0
        else:
            overall_score = int((correct_count / total_questions) * 100)
            
        # User Requirement: If user answers 3 or more questions correctly, score must be > 50%
        if correct_count >= 3 and overall_score <= 50:
            overall_score = 60
        
        # Save session to database if user_id provided
        if user_id:
            try:
                user_db.save_session(user_id, subject, difficulty, overall_score, session_data)
            except Exception as e:
                print(f"Error saving session: {e}")
        
        # Generate AI Recommendations
        try:
            # Identify weak areas based on messages (simplified logic for now)
            # In a real app, we'd track per-question correctness
            weak_concepts = ["General Understanding"] 
            ai_recs = chat_agent.generate_recommendations(subject, weak_concepts, difficulty)
            recommendations = ai_recs.get("recommendations", [])
        except Exception as e:
            print(f"AI Recommendation error: {e}")
            recommendations = [
                {"title": f"{subject} Fundamentals", "channel": "Crash Course", "query": f"{subject} crash course"},
                {"title": f"Advanced {subject} Concepts", "channel": "Khan Academy", "query": f"{subject} khan academy"},
                {"title": f"{subject} Practice Problems", "channel": "Organic Chemistry Tutor", "query": f"{subject} practice problems"}
            ]

        return {
            "overall_score": overall_score,
            "strengths": [
                "Good engagement with the material",
                "Thoughtful responses to questions",
                "Strong conceptual understanding"
            ],
            "weaknesses": [
                "Could benefit from more practice",
                "Review fundamental concepts for better retention"
            ],
            "recommendations": recommendations
        }
    except Exception as e:
        print(f"Analysis error: {e}")
        return {
            "overall_score": 0,
            "strengths": ["Good effort", "Active participation"],
            "weaknesses": ["Need more practice"],
            "recommendations": [
                {"title": "Review Basics", "channel": "General", "query": "study basics"}
            ]
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
