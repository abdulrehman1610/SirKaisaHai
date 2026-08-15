import sqlite3

def clean_test_users():
    db_path = 'd:/Experiments with AI/sirkaisahai/backend/sirkaisahai.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Clear all test users and logs
    cursor.execute("DELETE FROM verified_users")
    cursor.execute("DELETE FROM teacher_creation_logs")
    cursor.execute("DELETE FROM teacher_submission_logs")
    cursor.execute("DELETE FROM review_votes")

    conn.commit()
    conn.close()
    print("All test users, creation logs, and submission logs wiped cleanly!")

if __name__ == "__main__":
    clean_test_users()
