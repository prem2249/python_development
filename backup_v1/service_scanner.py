from cve_scanner import check_vulnerable_version
import re

def extract_service_version(banner: str):
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

def analyze_services(open_ports):
    issues = []
    for port, banner in open_ports.items():
        service, version = extract_service_version(banner)
        if not service:
            service = "Unknown"

        # Weak config checks
        if service.lower() == "ftp" and "anonymous" in banner.lower():
            issues.append(f"Port {port}: FTP allows anonymous login")
        if service.lower() == "telnet":
            issues.append(f"Port {port}: Telnet is insecure (plaintext)")

        # Dynamic CVE lookup
        vuln = check_vulnerable_version(service, version)
        if vuln:
            issues.append(f"Port {port}: {vuln}")

        if not version:
            issues.append(f"Port {port}: {service} detected (version unknown)")

    return issues