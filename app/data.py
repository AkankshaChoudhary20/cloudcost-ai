from app.models import ResourceMetric, ServiceCost

MOCK_COSTS = [
    ServiceCost(service="Amazon Elastic Compute Cloud - Compute", amount=620.50),
    ServiceCost(service="Amazon Simple Storage Service", amount=215.00),
    ServiceCost(service="Amazon Relational Database Service", amount=305.00),
    ServiceCost(service="AWS Lambda", amount=100.00),
]

MOCK_RESOURCES = [
    ResourceMetric(resource_id="i-0demo123", resource_type="ec2", monthly_cost=160.00, cpu_utilization_pct=8.2),
    ResourceMetric(resource_id="i-0demo456", resource_type="ec2", monthly_cost=240.00, cpu_utilization_pct=17.4),
    ResourceMetric(resource_id="vol-0demo789", resource_type="ebs", monthly_cost=72.00, storage_utilization_pct=12.0),
    ResourceMetric(resource_id="bucket-demo-logs", resource_type="s3", monthly_cost=85.00, storage_utilization_pct=35.0),
]
