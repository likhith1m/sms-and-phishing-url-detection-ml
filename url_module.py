import re
import math
from urllib.parse import urlparse

def calculate_entropy(domain):
    prob = [float(domain.count(c)) / len(domain) for c in dict.fromkeys(list(domain))]
    entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob])
    return entropy

def analyze_url(url):
    risk_score = 0
    reasons = []

    url = url.lower()
    parsed = urlparse(url)
    domain = parsed.netloc

    if url.startswith("http://"):
        risk_score += 20
        reasons.append("Insecure HTTP protocol")

    if re.match(r"\d+\.\d+\.\d+\.\d+", domain):
        risk_score += 30
        reasons.append("IP address used instead of domain")

    suspicious_words = ["login", "verify", "secure", "bank", "account"]
    for word in suspicious_words:
        if word in url:
            risk_score += 15
            reasons.append(f"Phishing keyword detected: {word}")

    suspicious_tlds = [".xyz", ".top", ".tk", ".ml"]
    for tld in suspicious_tlds:
        if domain.endswith(tld):
            risk_score += 20
            reasons.append(f"Suspicious TLD: {tld}")

    entropy = calculate_entropy(domain)
    if entropy > 4:
        risk_score += 15
        reasons.append("High domain randomness detected")

    return {
        "risk_score": min(risk_score, 100),
        "reasons": reasons
    }