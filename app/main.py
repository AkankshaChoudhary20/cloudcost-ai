from fastapi import FastAPI
from app.config import get_settings
from app.explainer import explain_analysis
from app.models import AnalysisResponse, ExplainRequest, ExplainResponse, Recommendation, ServiceCost
from app.service import CostAnalysisService

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version, description="AI-assisted AWS FinOps recommendation API")

@app.get("/")
def root() -> dict[str, str]:
    return {"name": settings.app_name, "docs": "/docs"}

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy", "mode": "mock" if settings.use_mock_data else "aws"}

@app.get("/api/v1/costs", response_model=list[ServiceCost])
def costs() -> list[ServiceCost]:
    return CostAnalysisService().provider.get_monthly_costs()

@app.get("/api/v1/recommendations", response_model=list[Recommendation])
def recommendations() -> list[Recommendation]:
    return CostAnalysisService().analyze().recommendations

@app.get("/api/v1/analysis", response_model=AnalysisResponse)
def analysis() -> AnalysisResponse:
    return CostAnalysisService().analyze()

@app.post("/api/v1/explain", response_model=ExplainResponse)
def explain(request: ExplainRequest) -> ExplainResponse:
    explanation, provider = explain_analysis(request.analysis)
    return ExplainResponse(explanation=explanation, provider=provider)
