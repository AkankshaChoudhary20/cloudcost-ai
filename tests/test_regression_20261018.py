import unittest
from app.models import ResourceMetric
from app.recommendations import build_recommendations

class RoundedSavingsTests(unittest.TestCase):
    def test_subcent_savings_do_not_create_zero_value_recommendations(self):
        for kind in ['ec2', 'ebs', 's3']:
            resource = ResourceMetric(resource_id='tiny', resource_type=kind, monthly_cost=.001, cpu_utilization_pct=5, storage_utilization_pct=5)
            self.assertEqual(build_recommendations([resource]), [])

    def test_positive_rounded_savings_remain(self):
        resource = ResourceMetric(resource_id='paid', resource_type='ec2', monthly_cost=100, cpu_utilization_pct=5)
        self.assertEqual(build_recommendations([resource])[0].estimated_monthly_savings, 60)
