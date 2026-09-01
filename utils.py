import re
import pandas as pd
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_csv(file_path):
    df = pd.read_csv(file_path)
    return " ".join(df.astype(str).values.flatten())

def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_features(email_text):
    suspicious_keywords = ["login", "verify", "update", "password", "bank", "click"]
    url_pattern = r"http[s]?://\S+"

    features = {
        "has_url": bool(re.search(url_pattern, email_text)),
        "keyword_hits": sum(word in email_text.lower() for word in suspicious_keywords),
        "length": len(email_text)
    }
    return features