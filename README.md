# Vulnerability Scanner

A lightweight Flask web application that scans a target (IP, hostname, or URL) for open ports, extracts service banners, checks for weak configurations, and queries the NVD CVE API for known vulnerabilities. Results are displayed as interactive, color‑coded cards with collapsible details and can be downloaded as plaintext reports.

---

## Features
- **Port scanning**: Common ports, custom ranges, or user‑defined lists.
- **Banner grabbing**: Extracts service/version information dynamically.
- **Weak configuration checks**: Flags insecure defaults (e.g., Telnet, anonymous FTP).
- **CVE lookup**: Queries NVD API for vulnerabilities based on service/version.
- **Severity scoring**: Uses CVSS scores to classify vulnerabilities (High/Medium/Low).
- **Interactive UI**: Collapsible cards with color coding and fix suggestions.
- **Report download**: Save results as plaintext for documentation.

---


---

## Installation

1. Step1: Clone the repository:
    ```bash
    git clone https://github.com/yourusername/vulnerability-scanner.git
    cd vulnerability-scanner

2. Step2: Environment Setup
    python -m venv venv

    # Windows
    venv\Scripts\activate

    # macOS/Linux
    source venv/bin/activate

    pip install -r requirements.txt

3. Step3: Run application
    python webapp.py
