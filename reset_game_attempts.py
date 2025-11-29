import sqlite3

def reset_attempts():
    db_path = "tutormate_users.db"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Delete all game attempts
        cursor.execute("DELETE FROM game_attempts")
        conn.commit()
        print("Successfully cleared game attempts.")
        
        conn.close()
    except Exception as e:
        print(f"Error resetting attempts: {e}")

if __name__ == "__main__":
    reset_attempts()
