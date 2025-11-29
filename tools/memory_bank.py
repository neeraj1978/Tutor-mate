import sqlite3
import json
import datetime
from typing import List, Dict, Any, Optional

class MemoryBank:
    def __init__(self, db_path: str = "tutor_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Student Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT,
                grade_level INTEGER
            )
        ''')

        # Concept Mastery Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS concept_mastery (
                student_id TEXT,
                concept_id TEXT,
                mastery_score REAL,
                last_practiced TIMESTAMP,
                last_mistake TEXT,
                history TEXT, -- JSON string of history
                PRIMARY KEY (student_id, concept_id)
            )
        ''')

        # Session History Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS session_history (
                session_id TEXT PRIMARY KEY,
                student_id TEXT,
                timestamp TIMESTAMP,
                quiz_data TEXT, -- JSON
                responses TEXT, -- JSON
                diagnosis TEXT -- JSON
            )
        ''')
        
        conn.commit()
        conn.close()

    def add_student(self, student_id: str, name: str, grade_level: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO students VALUES (?, ?, ?)', (student_id, name, grade_level))
        conn.commit()
        conn.close()

    def update_concept_mastery(self, student_id: str, concept_id: str, score_delta: float, mistake_summary: str = None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current state
        cursor.execute('SELECT mastery_score, history FROM concept_mastery WHERE student_id=? AND concept_id=?', (student_id, concept_id))
        row = cursor.fetchone()
        
        current_score = 0.0
        history = []
        
        if row:
            current_score = row[0]
            if row[1]:
                history = json.loads(row[1])
        
        new_score = max(0.0, min(1.0, current_score + score_delta))
        history.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "score_delta": score_delta,
            "mistake": mistake_summary
        })
        
        cursor.execute('''
            INSERT OR REPLACE INTO concept_mastery (student_id, concept_id, mastery_score, last_practiced, last_mistake, history)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (student_id, concept_id, new_score, datetime.datetime.now().isoformat(), mistake_summary, json.dumps(history)))
        
        conn.commit()
        conn.close()

    def get_student_mastery(self, student_id: str) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT concept_id, mastery_score, last_practiced FROM concept_mastery WHERE student_id=?', (student_id,))
        rows = cursor.fetchall()
        conn.close()
        return [{"concept_id": r[0], "mastery_score": r[1], "last_practiced": r[2]} for r in rows]

    def log_session(self, session_id: str, student_id: str, quiz_data: Dict, responses: Dict, diagnosis: Dict):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO session_history VALUES (?, ?, ?, ?, ?, ?)',
                       (session_id, student_id, datetime.datetime.now().isoformat(), 
                        json.dumps(quiz_data), json.dumps(responses), json.dumps(diagnosis)))
        conn.commit()
        conn.close()
