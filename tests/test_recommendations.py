from app.data import MOCK_RESOURCES
from app.recommendations import build_recommendations

def test_recommendations_are_ranked_and_have_savings():
    items = build_recommendations(MOCK_RESOURCES)
    assert len(items) == 4
    assert items[0].priority == "high"
    assert items[0].resource_id == "i-0demo123"
    assert sum(item.estimated_monthly_savings for item in items) > 0
