import sqlite3
import hashlib
import json
from datetime import datetime
import time

class UserDatabase:
    def __init__(self, db_path="tutormate_users.db"):
        self.db_path = db_path
        self._init_db()
    
    def _get_conn(self):
        """Get a database connection with timeout and WAL mode"""
        conn = sqlite3.connect(self.db_path, timeout=30.0) # 30s timeout
        conn.execute("PRAGMA journal_mode=WAL") # Write-Ahead Logging for concurrency
        return conn

    def _init_db(self):
        """Initialize the database with users and sessions tables"""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    grade_level TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Check if grade_level column exists (for migration)
            try:
                cursor.execute("SELECT grade_level FROM users LIMIT 1")
            except sqlite3.OperationalError:
                print("Migrating database: Adding grade_level column")
                try:
                    cursor.execute("ALTER TABLE users ADD COLUMN grade_level TEXT")
                except sqlite3.OperationalError:
                    pass # Column might have been added by another process
            
            # Sessions table to track learning sessions
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    subject TEXT NOT NULL,
                    difficulty TEXT NOT NULL,
                    score INTEGER,
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    session_data TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            conn.commit()
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, name, email, password, grade_level="College Year 1"):
        """Register a new user"""
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                
                password_hash = self.hash_password(password)
                cursor.execute(
                    "INSERT INTO users (name, email, password_hash, grade_level) VALUES (?, ?, ?, ?)",
                    (name, email, password_hash, grade_level)
                )
                
                user_id = cursor.lastrowid
                conn.commit()
                
                return {"success": True, "user_id": user_id, "name": name, "email": email, "grade_level": grade_level}
        except sqlite3.IntegrityError:
            return {"success": False, "error": "Email already registered"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def login_user(self, email, password):
        """Authenticate user"""
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                
                password_hash = self.hash_password(password)
                cursor.execute(
                    "SELECT id, name, email, grade_level FROM users WHERE email = ? AND password_hash = ?",
                    (email, password_hash)
                )
                
                user = cursor.fetchone()
                
                if user:
                    return {
                        "success": True,
                        "user": {
                            "id": user[0], 
                            "name": user[1], 
                            "email": user[2],
                            "grade_level": user[3] or "College Year 1"
                        }
                    }
                else:
                    return {"success": False, "error": "Invalid credentials"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def save_session(self, user_id, subject, difficulty, score, session_data):
        """Save a learning session"""
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    "INSERT INTO sessions (user_id, subject, difficulty, score, session_data) VALUES (?, ?, ?, ?, ?)",
                    (user_id, subject, difficulty, score, json.dumps(session_data))
                )
                conn.commit()
                return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_user_sessions(self, user_id, limit=10):
        """Get recent sessions for a user"""
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    """SELECT subject, difficulty, score, completed_at, session_data 
                       FROM sessions 
                       WHERE user_id = ? 
                       ORDER BY completed_at DESC 
                       LIMIT ?""",
                    (user_id, limit)
                )
                
                sessions = []
                for row in cursor.fetchall():
                    sessions.append({
                        "subject": row[0],
                        "difficulty": row[1],
                        "score": row[2],
                        "completed_at": row[3],
                        "session_data": json.loads(row[4]) if row[4] else {}
                    })
                return sessions
        except Exception as e:
            print(f"Error fetching sessions: {e}")
            return []
    
    def calculate_streak(self, user_id):
        """Calculate user's active learning streak (consecutive days with sessions)"""
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                
                # Get all session dates for this user, ordered by date descending
                cursor.execute(
                    """SELECT DISTINCT DATE(completed_at) as session_date
                       FROM sessions 
                       WHERE user_id = ? 
                       ORDER BY session_date DESC""",
                    (user_id,)
                )
                
                dates = [row[0] for row in cursor.fetchall()]
                
                if not dates:
                    return 0
                
                # Calculate streak from most recent date
                from datetime import datetime, timedelta
                
                streak = 0
                today = datetime.now().date()
                
                # Convert string dates to date objects
                session_dates = [datetime.strptime(d, '%Y-%m-%d').date() for d in dates]
                
                # Check if there's a session today or yesterday (to count current streak)
                most_recent = session_dates[0]
                if (today - most_recent).days > 1:
                    # Streak is broken if last session was more than 1 day ago
                    return 0
                
                # Count consecutive days
                streak = 1
                for i in range(len(session_dates) - 1):
                    current_date = session_dates[i]
                    next_date = session_dates[i + 1]
                    
                    # Check if dates are consecutive
                    if (current_date - next_date).days == 1:
                        streak += 1
                    else:
                        break
                
                return streak
                
        except Exception as e:
            print(f"Error calculating streak: {e}")
            return 0
    
    def get_user_stats(self, user_id):
        """Get user statistics"""
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                
                # Total sessions
                cursor.execute("SELECT COUNT(*) FROM sessions WHERE user_id = ?", (user_id,))
                total_sessions = cursor.fetchone()[0]
                
                # Average score
                cursor.execute("SELECT AVG(score) FROM sessions WHERE user_id = ? AND score IS NOT NULL", (user_id,))
                avg_score = cursor.fetchone()[0] or 0
                
                # Recent sessions by subject
                cursor.execute(
                    """SELECT subject, COUNT(*) as count, AVG(score) as avg_score
                       FROM sessions 
                       WHERE user_id = ? 
                       GROUP BY subject""",
                    (user_id,)
                )
                
                subjects = []
                for row in cursor.fetchall():
                    subjects.append({
                        "subject": row[0],
                        "count": row[1],
                        "avg_score": round(row[2] or 0, 1)
                    })
                
                # Calculate streak
                streak = self.calculate_streak(user_id)
                
                return {
                    "total_sessions": total_sessions,
                    "average_score": round(avg_score, 1),
                    "subjects": subjects,
                    "streak": streak
                }
        except Exception as e:
            print(f"Error fetching stats: {e}")
            return {
                "total_sessions": 0,
                "average_score": 0,
                "subjects": [],
                "streak": 0
            }

    def record_game_attempt(self, user_id, window_id, score):
        """Record a game attempt"""
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                
                # Create table if not exists (lazy init for this feature)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS game_attempts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        window_id INTEGER NOT NULL,
                        score INTEGER,
                        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')
                
                cursor.execute(
                    "INSERT INTO game_attempts (user_id, window_id, score) VALUES (?, ?, ?)",
                    (user_id, window_id, score)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error recording game attempt: {e}")
            return False

    def has_played_window(self, user_id, window_id):
        """Check if user has already played in this window"""
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                
                # Create table if not exists
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS game_attempts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        window_id INTEGER NOT NULL,
                        score INTEGER,
                        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')
                
                cursor.execute(
                    "SELECT 1 FROM game_attempts WHERE user_id = ? AND window_id = ?",
                    (user_id, window_id)
                )
                return cursor.fetchone() is not None
        except Exception as e:
            print(f"Error checking game attempt: {e}")
            return False

    def get_last_game_attempt(self, user_id):
        """Get the last game attempt for a user"""
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                
                # Create table if not exists (just in case)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS game_attempts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        window_id INTEGER NOT NULL,
                        score INTEGER,
                        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')
                
                cursor.execute(
                    """SELECT score, completed_at, window_id 
                       FROM game_attempts 
                       WHERE user_id = ? 
                       ORDER BY completed_at DESC 
                       LIMIT 1""",
                    (user_id,)
                )
                
                row = cursor.fetchone()
                if row:
                    return {
                        "score": row[0],
                        "completed_at": row[1],
                        "window_id": row[2]
                    }
                return None
        except Exception as e:
            print(f"Error fetching last game attempt: {e}")
            return None
