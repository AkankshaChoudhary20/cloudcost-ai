from typing import Literal
from pydantic import BaseModel, Field

class ServiceCost(BaseModel):
    service: str
    amount: float = Field(ge=0)
    currency: str = "USD"

class ResourceMetric(BaseModel):
    resource_id: str
    resource_type: Literal["ec2", "ebs", "s3"]
    monthly_cost: float = Field(ge=0)
    cpu_utilization_pct: float | None = Field(default=None, ge=0, le=100)
    storage_utilization_pct: float | None = Field(default=None, ge=0, le=100)

class Recommendation(BaseModel):
    category: Literal["compute", "storage"]
    resource_id: str
    title: str
    reason: str
    estimated_monthly_savings: float = Field(ge=0)
    priority: Literal["high", "medium", "low"]
    confidence: float = Field(ge=0, le=1)

class AnalysisResponse(BaseModel):
    monthly_spend: float
    potential_monthly_savings: float
    savings_percentage: float
    costs: list[ServiceCost]
    recommendations: list[Recommendation]

class ExplainRequest(BaseModel):
    analysis: AnalysisResponse

class ExplainResponse(BaseModel):
    explanation: str
    provider: str
