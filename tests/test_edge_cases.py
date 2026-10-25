from datetime import date
from types import SimpleNamespace
from unittest.mock import Mock
from app import aws

def test_cost_explorer_pages_are_aggregated_before_rounding(monkeypatch):
    def page(amount, **extra):
        return {"ResultsByTime": [{"Groups": [{"Keys": ["EC2"], "Metrics": {
            "UnblendedCost": {"Amount": amount, "Unit": "USD"}}}]}], **extra}
    client = Mock()
    client.get_cost_and_usage.side_effect = [page("1.004", NextPageToken="next"), page("2.004")]
    monkeypatch.setattr(aws.boto3, 'client', lambda *a, **kw: client)
    class Today(date):
        @classmethod
        def today(cls): return cls(2026, 10, 25)
    monkeypatch.setattr(aws, 'date', Today)
    provider = aws.AWSDataProvider()
    provider.settings = SimpleNamespace(use_mock_data=False, aws_region='us-east-1')
    costs = provider.get_monthly_costs()
    assert len(costs) == 1
    assert costs[0].amount == 3.01
    assert client.get_cost_and_usage.call_args_list[1].kwargs['NextPageToken'] == 'next'
