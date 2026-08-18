import re
import sqlite3
import secrets
import string

class PasswordStrengthAnalyzer:
    def __init__(self, db_path="passwords.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS old_passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password TEXT UNIQUE
            )
        """)
        self.conn.commit()

    def check_length(self, password):
        return len(password) >= 8

    def check_complexity(self, password):
        has_upper = bool(re.search(r"[A-Z]", password))
        has_lower = bool(re.search(r"[a-z]", password))
        has_digit = bool(re.search(r"\d", password))
        has_special = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
        return has_upper and has_lower and has_digit and has_special

    def check_uniqueness(self, password):
        return not re.search(r"(.)\1{2,}", password)

    def check_reuse(self, password):
        self.cursor.execute("SELECT * FROM old_passwords WHERE password=?", (password,))
        return self.cursor.fetchone() is None

    def analyze(self, password):
        score = 0
        feedback = []

        if self.check_length(password):
            score += 25
        else:
            feedback.append("Password too short (min 8 chars).")

        if self.check_complexity(password):
            score += 25
        else:
            feedback.append("Use uppercase, lowercase, digits, and special chars.")

        if self.check_uniqueness(password):
            score += 25
        else:
            feedback.append("Avoid repeated characters or sequences.")

        if self.check_reuse(password):
            score += 25
        else:
            feedback.append("Password has been used before.")

        strength = "Weak"
        if score >= 75:
            strength = "Strong"
        elif score >= 50:
            strength = "Medium"

        return {"score": score, "strength": strength, "feedback": feedback}

    def suggest_password(self, length=12):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def save_password(self, password):
        try:
            self.cursor.execute("INSERT INTO old_passwords (password) VALUES (?)", (password,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass