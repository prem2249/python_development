import requests

NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def check_vulnerable_version(service: str, version: str):
    if not service or not version:
        return None

    try:
        query = f"{service} {version}"
        params = {"keywordSearch": query, "resultsPerPage": 3}
        resp = requests.get(NVD_API, params=params, timeout=5)

        if resp.status_code == 200:
            data = resp.json()
            if "vulnerabilities" in data and data["vulnerabilities"]:
                results = []
                for vuln in data["vulnerabilities"]:
                    cve_id = vuln["cve"]["id"]
                    description = vuln["cve"]["descriptions"][0]["value"]
                    score = None
                    severity = "low"
                    metrics = vuln["cve"].get("metrics", {})
                    if "cvssMetricV31" in metrics:
                        score = metrics["cvssMetricV31"][0]["cvssData"]["baseScore"]
                    elif "cvssMetricV30" in metrics:
                        score = metrics["cvssMetricV30"][0]["cvssData"]["baseScore"]
                    elif "cvssMetricV2" in metrics:
                        score = metrics["cvssMetricV2"][0]["cvssData"]["baseScore"]

                    if score:
                        if score >= 9.0:
                            severity = "high"
                        elif score >= 5.0:
                            severity = "medium"
                        else:
                            severity = "low"

                    results.append({
                        "cve_id": cve_id,
                        "description": description,
                        "score": score,
                        "severity": severity,
                        "fix": "Update to the latest stable version or apply vendor patch."
                    })
                return results
    except Exception as e:
        return [{"cve_id": "Error", "description": str(e), "severity": "low"}]

    return None
