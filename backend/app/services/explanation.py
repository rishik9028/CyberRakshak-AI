import os
import json
from typing import List, Optional
from dataclasses import dataclass

from app.schemas.url_analysis import Indicator, RiskLevel
from app.services.threat_intel import ThreatIntelResult


@dataclass
class ExplanationContext:
    url: str
    risk_score: int
    risk_level: RiskLevel
    indicators: List[Indicator]
    threat_intel: List[ThreatIntelResult]


TEMPLATE_EXPLANATIONS = {
    "urgency_language": "The link uses urgent language to pressure you into acting quickly without thinking.",
    "credential_request": "The link asks for passwords, personal info, or verification codes — legitimate companies rarely request these via unsolicited links.",
    "brand_impersonation": "The link appears to mimic a well-known brand but uses a different domain.",
    "shortened_url": "The link uses a URL shortener, which hides the real destination.",
    "suspicious_tld": "The link uses a high-risk domain extension often associated with abuse.",
    "ip_hostname": "The link uses an IP address instead of a proper domain name.",
    "long_url": "The link is unusually long, which can indicate obfuscation or tracking.",
    "excessive_subdomains": "The link has many subdomains, a common tactic to make the URL look familiar.",
    "non_https": "The link doesn't use HTTPS, meaning your connection isn't encrypted.",
    "at_symbol": "The link contains an @ symbol, which can be used to embed credentials or mislead.",
    "double_slash_redirect": "The link contains a double-slash pattern that may indicate an open redirect.",
    "hex_encoding": "The link contains hex-encoded characters, often used to hide malicious content.",
}


def generate_template_explanation(ctx: ExplanationContext) -> str:
    matched_indicators = [i for i in ctx.indicators if i.matched]
    
    if not matched_indicators:
        return "No suspicious indicators were detected in this URL."

    parts = [f"Risk Level: {ctx.risk_level.value} (Score: {ctx.risk_score}/100)"]
    parts.append("")
    parts.append("Why this link is suspicious:")

    for ind in matched_indicators:
        template = TEMPLATE_EXPLANATIONS.get(ind.name)
        if template:
            parts.append(f"• {template}")

    if ctx.threat_intel:
        malicious = [t for t in ctx.threat_intel if t.is_malicious]
        if malicious:
            parts.append("")
            parts.append("Threat intelligence matches:")
            for t in malicious:
                parts.append(f"• {t.provider}: {t.indicator} is flagged as malicious")

    parts.append("")
    parts.append("Recommendation: Do not click this link. Verify through official channels if unsure.")

    return "\n".join(parts)


async def generate_llm_explanation(ctx: ExplanationContext) -> Optional[str]:
    api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        import httpx

        indicator_summary = "\n".join(
            f"- {i.name}: {i.description} (matched: {i.matched})"
            for i in ctx.indicators if i.matched
        )

        prompt = f"""You are a cybersecurity assistant explaining why a URL is suspicious to a non-technical user.

URL: {ctx.url}
Risk Score: {ctx.risk_score}/100
Risk Level: {ctx.risk_level.value}

Matched Indicators:
{indicator_summary}

Write a clear, concise explanation (2-3 sentences) of why this link is dangerous. Avoid jargon. Do not make up information."""

        if os.getenv("ANTHROPIC_API_KEY"):
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": "claude-3-haiku-20240307",
                        "max_tokens": 300,
                        "messages": [{"role": "user", "content": prompt}],
                    },
                )
                if response.is_success:
                    data = response.json()
                    return data["content"][0]["text"].strip()

        elif os.getenv("OPENAI_API_KEY"):
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "gpt-4o-mini",
                        "max_tokens": 300,
                        "messages": [{"role": "user", "content": prompt}],
                    },
                )
                if response.is_success:
                    data = response.json()
                    return data["choices"][0]["message"]["content"].strip()

    except Exception:
        pass

    return None


async def generate_explanation(ctx: ExplanationContext) -> str:
    llm_result = await generate_llm_explanation(ctx)
    if llm_result:
        return llm_result

    return generate_template_explanation(ctx)