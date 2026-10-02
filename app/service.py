from app.aws import AWSDataProvider
from app.models import AnalysisResponse
from app.recommendations import build_recommendations

class CostAnalysisService:
    def __init__(self, provider: AWSDataProvider | None = None) -> None:
        self.provider = provider or AWSDataProvider()

    def analyze(self) -> AnalysisResponse:
        costs = self.provider.get_monthly_costs()
        recommendations = build_recommendations(self.provider.get_resource_metrics())
        spend = round(sum(item.amount for item in costs), 2)
        savings = round(sum(item.estimated_monthly_savings for item in recommendations), 2)
        percentage = round((savings / spend * 100), 2) if spend else 0.0
        return AnalysisResponse(
            monthly_spend=spend,
            potential_monthly_savings=savings,
            savings_percentage=percentage,
            costs=costs,
            recommendations=recommendations,
        )
