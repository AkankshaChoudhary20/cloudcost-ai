import pytest
from pydantic import ValidationError
from app.models import ServiceCost, ResourceMetric, Recommendation, AnalysisResponse

@pytest.mark.parametrize('amount',[float('inf'),float('-inf'),float('nan')])
def test_nonfinite_amounts_are_rejected(amount):
    for model,values in [
        (ServiceCost,dict(service='EC2',amount=amount)),
        (ResourceMetric,dict(resource_id='i-test',resource_type='ec2',monthly_cost=amount)),
        (Recommendation,dict(category='compute',resource_id='i-test',title='Review',reason='Low CPU',estimated_monthly_savings=amount,priority='low',confidence=.5)),
    ]:
        with pytest.raises(ValidationError):model(**values)

@pytest.mark.parametrize('field',['monthly_spend','potential_monthly_savings','savings_percentage'])
def test_analysis_totals_must_be_finite(field):
    values=dict(monthly_spend=100,potential_monthly_savings=10,savings_percentage=10,costs=[],recommendations=[])
    values[field]=float('inf')
    with pytest.raises(ValidationError):AnalysisResponse(**values)
