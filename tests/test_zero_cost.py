import unittest
from app.models import ResourceMetric
from app.recommendations import build_recommendations
class ZeroCostTests(unittest.TestCase):
    def test_free_resources_do_not_generate_savings_recommendations(self):
        resources=[ResourceMetric(resource_id=kind,resource_type=kind,monthly_cost=0,cpu_utilization_pct=1,storage_utilization_pct=1) for kind in ('ec2','ebs','s3')]
        self.assertEqual(build_recommendations(resources),[])
    def test_paid_resources_still_generate_recommendations(self):
        result=build_recommendations([ResourceMetric(resource_id='paid',resource_type='ec2',monthly_cost=100,cpu_utilization_pct=1)])
        self.assertEqual(result[0].estimated_monthly_savings,60)
