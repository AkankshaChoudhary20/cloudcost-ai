from datetime import date
import boto3
from app.config import get_settings
from app.data import MOCK_COSTS, MOCK_RESOURCES
from app.models import ResourceMetric, ServiceCost

class AWSDataProvider:
    def __init__(self) -> None:
        self.settings = get_settings()

    def get_monthly_costs(self) -> list[ServiceCost]:
        if self.settings.use_mock_data:
            return MOCK_COSTS
        today = date.today()
        start = today.replace(day=1).isoformat()
        end = today.isoformat()
        if start == end:
            return []
        client = boto3.client("ce", region_name=self.settings.aws_region)
        response = client.get_cost_and_usage(
            TimePeriod={"Start": start, "End": end},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
            GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
        )
        costs: list[ServiceCost] = []
        for period in response.get("ResultsByTime", []):
            for group in period.get("Groups", []):
                metric = group["Metrics"]["UnblendedCost"]
                costs.append(ServiceCost(
                    service=group["Keys"][0],
                    amount=round(float(metric["Amount"]), 2),
                    currency=metric["Unit"],
                ))
        return sorted(costs, key=lambda item: item.amount, reverse=True)

    def get_resource_metrics(self) -> list[ResourceMetric]:
        # v1 uses deterministic resource metrics. The interface is intentionally
        # isolated so CloudWatch/EC2/EBS collectors can replace this implementation.
        return MOCK_RESOURCES
