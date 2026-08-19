import re
import sqlite3
import secrets
import string
import math

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

    def check_repeats(self, password):
        # Case-insensitive check for any immediate repetition
        lowered = password.lower()

        # Detect aa, aA, Aa, AA, 11, !! etc.
        for i in range(len(lowered) - 1):
            if lowered[i] == lowered[i+1]:
                return False
        return True


    def check_sequences(self, password):
        sequences = [
            "abcdefghijklmnopqrstuvwxyz",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "0123456789"
        ]

        lowered = password.lower()

        # Check for consecutive sequences of length 2 or more
        for seq in sequences:
            for i in range(len(seq) - 1):
                # forward sequence (ab, bc, cd, 12, 23, 34)
                if seq[i:i+2] in lowered:
                    return False
                # longer forward sequences (abcd, 1234)
                if seq[i:i+4] in lowered:
                    return False
                # reverse sequences (ba, dc, 21, 4321)
                if seq[i:i+2][::-1] in lowered:
                    return False
                if seq[i:i+4][::-1] in lowered:
                    return False
        return True


    def check_dictionary(self, password):
        common_words = ["password", "admin", "welcome", "login", "user", "qwerty", "abc123"]
        for word in common_words:
            if word.lower() in password.lower():
                return False
        return True

    def analyze(self, password):
        feedback = []

        # Immediate Weak conditions
        if len(password) < 8:
            feedback.append("Password too short (minimum 8 characters, best practice is 12+).")
            return {"score": 0, "strength": "Weak", "feedback": feedback}

        if not self.check_repeats(password):
            feedback.append("Password contains repeated characters (e.g., aa, AA, 11, !!).")
            return {"score": 0, "strength": "Weak", "feedback": feedback}

        if not self.check_sequences(password):
            feedback.append("Password contains continuous sequences (e.g., abcd, 1234, ABCD).")
            return {"score": 0, "strength": "Weak", "feedback": feedback}

        if not self.check_dictionary(password):
            feedback.append("Password contains common weak words (e.g., 'password', 'admin').")
            return {"score": 0, "strength": "Weak", "feedback": feedback}

        #  Reuse check
        self.cursor.execute("SELECT * FROM old_passwords WHERE password=?", (password,))
        if self.cursor.fetchone():
            feedback.append("This password was used before. Please choose a new one.")
            return {"score": 0, "strength": "Weak", "feedback": feedback}

        # If none of the Weak conditions triggered, continue scoring
        score = 0

        # Length scoring
        if len(password) >= 12: score += 30
        elif len(password) >= 8: score += 20

        # Complexity scoring
        complexity = sum([
            bool(re.search(r"[A-Z]", password)),
            bool(re.search(r"[a-z]", password)),
            bool(re.search(r"\d", password)),
            bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
        ])
        if complexity == 4: score += 40
        else:
            feedback.append("Password must include uppercase, lowercase, digits, and special characters.")

        # Entropy scoring
        pool = 0
        if re.search(r"[a-z]", password): pool += 26
        if re.search(r"[A-Z]", password): pool += 26
        if re.search(r"\d", password): pool += 10
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): pool += 32
        entropy = len(password) * math.log2(pool) if pool else 0
        if entropy >= 60: score += 30
        else: feedback.append("Password entropy is low — try mixing more character types.")

        strength = "Weak"
        if score >= 80:
            strength = "Strong"
        elif score >= 50:
            strength = "Medium"

        return {"score": score, "strength": strength, "feedback": feedback}


    def suggest_password(self, length=14):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def save_password(self, password):
        # Check if password already exists
        self.cursor.execute("SELECT * FROM old_passwords WHERE password=?", (password,))
        existing = self.cursor.fetchone()

        if existing:
            # Already used before
            return {"status": "old", "message": "This password was used before. Please choose a new one."}
        else:
            # Save new password
            self.cursor.execute("INSERT INTO old_passwords (password) VALUES (?)", (password,))
            self.conn.commit()
            return {"status": "new", "message": "Password saved successfully."}