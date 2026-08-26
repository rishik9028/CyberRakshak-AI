import re
from urllib.parse import urlparse
from typing import List, Dict, Any
from dataclasses import dataclass

from app.schemas.url_analysis import Indicator, RiskLevel


@dataclass
class IndicatorResult:
    name: str
    description: str
    severity: str
    matched: bool


URGENCY_KEYWORDS = [
    r"urgent", r"immediate", r"act now", r"limited time", r"expires today",
    r"last chance", r"verify now", r"security alert", r"account suspended",
    r"unauthorized access", r"suspended", r"locked", r"blocked"
]

CREDENTIAL_KEYWORDS = [
    r"password", r"login", r"credential", r"username", r"otp", r"2fa",
    r"verification code", r"pin", r"secret", r"kyc", r"identity",
    r"social security", r"ssn", r"passport", r"driver.?license"
]

IMPERSONATION_KEYWORDS = [
    r"bank", r"paypal", r"amazon", r"microsoft", r"google", r"apple",
    r"facebook", r"instagram", r"whatsapp", r"telegram", r"linkedin",
    r"netflix", r"spotify", r"delivery", r"fedex", r"ups", r"usps",
    r"dhl", r"irs", r"tax", r"government", r"official"
]

SUSPICIOUS_TLDS = {
    ".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top", ".club",
    ".work", ".loan", ".download", ".click", ".bid", ".racing"
}

SHORTENERS = {
    "bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd",
    "buff.ly", "adf.ly", "short.link", "cutt.ly", "rb.gy", "v.gd"
}

KNOWN_BRANDS = {
    "google", "microsoft", "apple", "amazon", "facebook", "paypal",
    "netflix", "instagram", "whatsapp", "linkedin", "twitter", "github"
}


def extract_features(url: str) -> Dict[str, Any]:
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""

    features = {
        "scheme": parsed.scheme,
        "hostname": hostname,
        "path": path,
        "query": query,
        "port": parsed.port,
        "is_https": parsed.scheme == "https",
        "url_length": len(url),
        "hostname_length": len(hostname),
        "subdomain_count": max(0, len(hostname.split(".")) - 2) if hostname else 0,
        "has_ip_hostname": bool(re.match(r"^\d+\.\d+\.\d+\.\d+$", hostname)),
        "has_suspicious_tld": any(hostname.endswith(tld) for tld in SUSPICIOUS_TLDS),
        "is_shortener": hostname in SHORTENERS,
        "has_at_symbol": "@" in url,
        "has_double_slash_redirect": "//" in url[8:],
        "has_hex_encoding": bool(re.search(r"%[0-9a-fA-F]{2}", url)),
        "subdomains": hostname.split(".")[:-2] if len(hostname.split(".")) > 2 else [],
    }
    return features


def check_indicators(url: str, features: Dict[str, Any]) -> List[IndicatorResult]:
    results = []

    # Urgency indicators
    urgency_matched = any(re.search(kw, url, re.IGNORECASE) for kw in URGENCY_KEYWORDS)
    results.append(IndicatorResult(
        name="urgency_language",
        description="URL contains urgency-inducing language",
        severity="high",
        matched=urgency_matched
    ))

    # Credential/KYC request
    credential_matched = any(re.search(kw, url, re.IGNORECASE) for kw in CREDENTIAL_KEYWORDS)
    results.append(IndicatorResult(
        name="credential_request",
        description="URL requests credentials or personal information",
        severity="high",
        matched=credential_matched
    ))

    # Impersonation
    hostname_lower = features["hostname"].lower()
    impersonation_matched = any(
        brand in hostname_lower and not hostname_lower.endswith(f".{brand}.com")
        for brand in KNOWN_BRANDS
    )
    results.append(IndicatorResult(
        name="brand_impersonation",
        description="URL appears to impersonate a known brand",
        severity="high",
        matched=impersonation_matched
    ))

    # Shortened URL
    results.append(IndicatorResult(
        name="shortened_url",
        description="URL uses a known URL shortening service",
        severity="medium",
        matched=features["is_shortener"]
    ))

    # Suspicious TLD
    results.append(IndicatorResult(
        name="suspicious_tld",
        description="URL uses a suspicious or high-risk top-level domain",
        severity="medium",
        matched=features["has_suspicious_tld"]
    ))

    # IP as hostname
    results.append(IndicatorResult(
        name="ip_hostname",
        description="URL uses an IP address instead of a domain name",
        severity="high",
        matched=features["has_ip_hostname"]
    ))

    # Long URL
    results.append(IndicatorResult(
        name="long_url",
        description="URL is unusually long (potential obfuscation)",
        severity="low",
        matched=features["url_length"] > 100
    ))

    # Multiple subdomains
    results.append(IndicatorResult(
        name="excessive_subdomains",
        description="URL has an excessive number of subdomains",
        severity="medium",
        matched=features["subdomain_count"] > 3
    ))

    # Non-HTTPS
    results.append(IndicatorResult(
        name="non_https",
        description="URL does not use HTTPS",
        severity="medium",
        matched=not features["is_https"]
    ))

    # @ symbol in URL
    results.append(IndicatorResult(
        name="at_symbol",
        description="URL contains @ symbol (credential embedding attempt)",
        severity="high",
        matched=features["has_at_symbol"]
    ))

    # Double slash redirect
    results.append(IndicatorResult(
        name="double_slash_redirect",
        description="URL contains double slash after protocol (open redirect risk)",
        severity="medium",
        matched=features["has_double_slash_redirect"]
    ))

    # Hex encoding
    results.append(IndicatorResult(
        name="hex_encoding",
        description="URL contains hex-encoded characters (obfuscation)",
        severity="medium",
        matched=features["has_hex_encoding"]
    ))

    return results


def calculate_risk_score(indicators: List[IndicatorResult]) -> int:
    score = 0
    severity_weights = {"critical": 25, "high": 20, "medium": 10, "low": 5}

    for ind in indicators:
        if ind.matched:
            score += severity_weights.get(ind.severity.lower(), 10)

    return min(score, 100)


def get_risk_level(score: int) -> RiskLevel:
    if score >= 80:
        return RiskLevel.CRITICAL
    elif score >= 60:
        return RiskLevel.HIGH
    elif score >= 30:
        return RiskLevel.MEDIUM
    return RiskLevel.LOW


def analyze_url(url: str) -> Dict[str, Any]:
    features = extract_features(url)
    indicator_results = check_indicators(url, features)

    indicators = [
        Indicator(
            name=r.name,
            description=r.description,
            severity=r.severity,
            matched=r.matched
        )
        for r in indicator_results
    ]

    risk_score = calculate_risk_score(indicator_results)
    risk_level = get_risk_level(risk_score)

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "indicators": indicators,
        "features": features
    }