from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ThreatIntelIndicator:
    name: str
    value: str


@dataclass
class ThreatIntelResult:
    provider: str
    indicator: str
    result: Dict[str, Any]
    is_malicious: bool = False
    confidence: float = 0.0


class ThreatIntelProvider(ABC):
    @abstractmethod
    def check(self, indicators: List[ThreatIntelIndicator]) -> List[ThreatIntelResult]:
        pass

    @abstractmethod
    def is_enabled(self) -> bool:
        pass


class MockThreatIntelProvider(ThreatIntelProvider):
    def __init__(self, malicious_domains: Optional[set] = None):
        self.malicious_domains = malicious_domains or {
            "malicious.example.com",
            "phish.test",
            "scam.demo"
        }

    def check(self, indicators: List[ThreatIntelIndicator]) -> List[ThreatIntelResult]:
        results = []
        for ind in indicators:
            is_malicious = ind.value in self.malicious_domains
            results.append(ThreatIntelResult(
                provider="mock",
                indicator=ind.value,
                result={"listed": is_malicious, "source": "mock_database"},
                is_malicious=is_malicious,
                confidence=1.0 if is_malicious else 0.0
            ))
        return results

    def is_enabled(self) -> bool:
        return True


class ThreatIntelManager:
    def __init__(self):
        self.providers: List[ThreatIntelProvider] = [MockThreatIntelProvider()]

    def add_provider(self, provider: ThreatIntelProvider):
        if provider.is_enabled():
            self.providers.append(provider)

    def check_all(self, indicators: List[ThreatIntelIndicator]) -> List[ThreatIntelResult]:
        all_results = []
        for provider in self.providers:
            try:
                results = provider.check(indicators)
                all_results.extend(results)
            except Exception:
                continue
        return all_results


threat_intel_manager = ThreatIntelManager()