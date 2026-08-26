from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.models import Analysis, InputType, RiskLevel, ThreatIntelligenceResult
from app.schemas.url_analysis import (
    URLAnalysisRequest,
    URLAnalysisResponse,
    Indicator,
    ThreatIntelResult,
)
from app.services.url_analyzer import analyze_url
from app.services.threat_intel import threat_intel_manager, ThreatIntelIndicator
from app.services.explanation import generate_explanation, ExplanationContext

router = APIRouter()


@router.post("/analyze/url", response_model=URLAnalysisResponse, status_code=status.HTTP_201_CREATED)
async def analyze_url_endpoint(
    request: URLAnalysisRequest,
    db: Session = Depends(get_db),
):
    result = analyze_url(str(request.url))

    intel_indicators = [
        ThreatIntelIndicator(name="domain", value=result["features"]["hostname"])
    ]
    threat_intel_results = threat_intel_manager.check_all(intel_indicators)

    intel_schema = [
        ThreatIntelResult(
            provider=r.provider,
            indicator=r.indicator,
            result=r.result,
        )
        for r in threat_intel_results
    ]

    ctx = ExplanationContext(
        url=str(request.url),
        risk_score=result["risk_score"],
        risk_level=result["risk_level"],
        indicators=result["indicators"],
        threat_intel=threat_intel_results,
    )

    explanation = None
    if request.include_explanation:
        explanation = await generate_explanation(ctx)

    analysis = Analysis(
        user_id=None,
        input_type=InputType.URL,
        input_summary=str(request.url)[:500],
        risk_score=result["risk_score"],
        risk_level=result["risk_level"],
        indicators=[ind.model_dump() for ind in result["indicators"]],
        result_summary=explanation,
    )
    db.add(analysis)
    db.flush()

    for t in threat_intel_results:
        if t.is_malicious:
            db.add(ThreatIntelligenceResult(
                analysis_id=analysis.id,
                provider=t.provider,
                indicator=t.indicator,
                result=t.result,
            ))

    db.commit()
    db.refresh(analysis)

    return URLAnalysisResponse(
        analysis_id=analysis.id,
        input_type=InputType.URL,
        risk_score=analysis.risk_score,
        risk_level=analysis.risk_level,
        indicators=result["indicators"],
        threat_intel=intel_schema,
        explanation=explanation,
        created_at=analysis.created_at,
    )