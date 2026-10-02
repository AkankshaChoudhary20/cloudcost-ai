from app.models import Recommendation, ResourceMetric

def build_recommendations(resources: list[ResourceMetric]) -> list[Recommendation]:
    recommendations: list[Recommendation] = []
    for resource in resources:
        if resource.resource_type == "ec2" and resource.cpu_utilization_pct is not None:
            if resource.cpu_utilization_pct < 10:
                savings = round(resource.monthly_cost * 0.60, 2)
                recommendations.append(Recommendation(
                    category="compute", resource_id=resource.resource_id,
                    title="Rightsize underutilized EC2 instance",
                    reason=f"Average CPU utilization is only {resource.cpu_utilization_pct:.1f}%.",
                    estimated_monthly_savings=savings, priority="high", confidence=0.92,
                ))
            elif resource.cpu_utilization_pct < 25:
                savings = round(resource.monthly_cost * 0.35, 2)
                recommendations.append(Recommendation(
                    category="compute", resource_id=resource.resource_id,
                    title="Review EC2 instance size",
                    reason=f"Average CPU utilization is {resource.cpu_utilization_pct:.1f}%, below the 25% review threshold.",
                    estimated_monthly_savings=savings, priority="medium", confidence=0.82,
                ))
        if resource.resource_type in {"ebs", "s3"} and resource.storage_utilization_pct is not None and resource.storage_utilization_pct < 40:
            savings = round(resource.monthly_cost * 0.30, 2)
            recommendations.append(Recommendation(
                category="storage", resource_id=resource.resource_id,
                title="Optimize low-utilization storage",
                reason=f"Storage utilization is {resource.storage_utilization_pct:.1f}%. Review lifecycle/tiering or allocated capacity.",
                estimated_monthly_savings=savings, priority="medium", confidence=0.78,
            ))
    rank = {"high": 0, "medium": 1, "low": 2}
    return sorted(recommendations, key=lambda item: (rank[item.priority], -item.estimated_monthly_savings))
