from app.aws import AWSDataProvider
from app.data import MOCK_COSTS, MOCK_RESOURCES

def test_mock_results_do_not_expose_shared_mutable_models(monkeypatch):
    monkeypatch.setenv('USE_MOCK_DATA', 'true')
    from app.config import get_settings
    get_settings.cache_clear()
    provider = AWSDataProvider()
    costs = provider.get_monthly_costs(); resources = provider.get_resource_metrics()
    assert costs[0] is not MOCK_COSTS[0]
    assert resources[0] is not MOCK_RESOURCES[0]
    costs[0].amount = 0; resources[0].monthly_cost = 0
    costs.clear(); resources.clear()
    assert provider.get_monthly_costs()[0].amount == MOCK_COSTS[0].amount
    assert provider.get_resource_metrics()[0].monthly_cost == MOCK_RESOURCES[0].monthly_cost
    get_settings.cache_clear()
