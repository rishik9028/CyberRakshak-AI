from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, Text, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.base import Base


class UserRole(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class InputType(str, enum.Enum):
    URL = "URL"
    MESSAGE = "MESSAGE"
    QR = "QR"
    SCREENSHOT = "SCREENSHOT"


class RiskLevel(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(100))
    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)
    preferred_language = Column(String(10), default="en")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    analyses = relationship("Analysis", back_populates="user", lazy="dynamic")


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    input_type = Column(SQLEnum(InputType), nullable=False)
    input_summary = Column(Text, nullable=True)
    risk_score = Column(Integer, nullable=False, default=0)
    risk_level = Column(SQLEnum(RiskLevel), nullable=False, default=RiskLevel.LOW)
    indicators = Column(JSON, nullable=False, default=dict)
    result_summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    user = relationship("User", back_populates="analyses")


class ThreatIntelligenceResult(Base):
    __tablename__ = "threat_intelligence_results"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id", ondelete="CASCADE"), nullable=False, index=True)
    provider = Column(String(50), nullable=False)
    indicator = Column(String(255), nullable=False)
    result = Column(JSON, nullable=False, default=dict)
    checked_at = Column(DateTime(timezone=True), server_default=func.now())

    analysis = relationship("Analysis", lazy="joined")


class ScamCategory(Base):
    __tablename__ = "scam_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)


class ScamReport(Base):
    __tablename__ = "scam_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    category_id = Column(Integer, ForeignKey("scam_categories.id", ondelete="SET NULL"), nullable=True)
    description = Column(Text, nullable=False)
    channel = Column(String(50), nullable=True)
    approximate_location = Column(String(255), nullable=True)
    latitude_approx = Column(Integer, nullable=True)
    longitude_approx = Column(Integer, nullable=True)
    reported_url = Column(Text, nullable=True)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", foreign_keys=[user_id])
    category = relationship("ScamCategory")
    reviewer = relationship("User", foreign_keys=[reviewed_by])