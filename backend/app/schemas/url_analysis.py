from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class InputType(str, Enum):
    URL = "URL"
    MESSAGE = "MESSAGE"
    QR = "QR"
    SCREENSHOT = "SCREENSHOT"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class URLAnalysisRequest(BaseModel):
    url: HttpUrl = Field(..., description="URL to analyze")
    include_explanation: bool = Field(default=True, description="Include human-readable explanation")


class Indicator(BaseModel):
    name: str
    description: str
    severity: str
    matched: bool


class ThreatIntelResult(BaseModel):
    provider: str
    indicator: str
    result: Dict[str, Any]


class URLAnalysisResponse(BaseModel):
    analysis_id: int
    input_type: InputType
    risk_score: int
    risk_level: RiskLevel
    indicators: List[Indicator]
    threat_intel: List[ThreatIntelResult] = []
    explanation: Optional[str] = None
    created_at: datetime


class AuthRegisterRequest(BaseModel):
    email: str
    password: str
    display_name: Optional[str] = None


class AuthLoginRequest(BaseModel):
    email: str
    password: str


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    id: int
    email: str
    display_name: Optional[str] = None
    role: str
    preferred_language: str
    created_at: datetime

    class Config:
        from_attributes = True