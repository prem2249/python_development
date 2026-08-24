import socket
import datetime
import re
import os
from urllib.parse import urlparse
from service_scanner import analyze_services
from cve_scanner import check_vulnerable_version

def normalize_target(target: str) -> str:
    parsed = urlparse(target)
    if parsed.scheme:
        return parsed.netloc
    return target.strip("/")

def sanitize_filename(target: str) -> str:
    return re.sub(r'[^A-Za-z0-9.-]', '_', target)

def resolve_target(target: str):
    try:
        return socket.gethostbyname(target)
    except Exception as e:
        print(f"DNS resolution failed: {e}")
        return None

# Common ports list
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 993, 995, 3306, 8080]

def full_port_scan(target, mode="common", start=1, end=1024, custom_ports=None):
    """
    mode = "common" → scan common ports
    mode = "range"  → scan from start to end
    mode = "list"   → scan custom_ports list
    """
    if mode == "common":
        ports = COMMON_PORTS
    elif mode == "range":
        ports = range(start, end + 1)
    elif mode == "list" and custom_ports:
        ports = custom_ports
    else:
        ports = COMMON_PORTS

    open_ports = {}
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((target, port))
            if result == 0:
                try:
                    sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                    banner = sock.recv(1024).decode(errors="ignore").strip()
                except:
                    banner = "Unknown service"
                open_ports[port] = banner
            sock.close()
        except:
            pass
    return open_ports

def extract_service_version(banner: str):
    """
    Extract service and version from banner dynamically.
    """
    if not banner or banner == "Unknown service":
        return None, None
    match = re.search(r"([A-Za-z0-9\-_]+)[/ ]([0-9]+\.[0-9]+(\.[0-9]+)?)", banner)
    if match:
        return match.group(1), match.group(2)
    parts = banner.split()
    if len(parts) >= 2:
        return parts[0], parts[1]
    elif parts:
        return parts[0], None
    return None, None

def generate_report_text(target, open_ports):
    report = "=== Vulnerability Scan Report ===\n"
    report += f"Target: {target}\n"
    report += f"Date: {datetime.datetime.now()}\n\n"
    if open_ports:
        report += "Open Ports:\n"
        for port, banner in open_ports.items():
            report += f" - Port {port} -> {banner}\n"
            service, version = extract_service_version(banner)
            vuln = check_vulnerable_version(service, version)   # ✅ now passes both args
            if vuln:
                report += f"   [!] {vuln}\n"
        issues = analyze_services(open_ports)
        if issues:
            report += "\nIssues Found:\n"
            for issue in issues:
                report += f" - {issue}\n"
    else:
        report += "No open ports detected.\n"
    return report

def save_report(target, report_text):
    os.makedirs("reports", exist_ok=True)
    safe_target = sanitize_filename(normalize_target(target))
    filename = os.path.join("reports", f"vuln_report_{safe_target}.txt")
    # ✅ ensure UTF-8 encoding to avoid UnicodeEncodeError
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_text)
    return filename