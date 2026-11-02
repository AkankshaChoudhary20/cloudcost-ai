from types import SimpleNamespace
from unittest.mock import Mock, patch
import pytest
from app.aws import AWSDataProvider

def test_repeated_cost_explorer_token_fails_instead_of_looping():
    provider = AWSDataProvider()
    provider.settings = SimpleNamespace(use_mock_data=False, aws_region='us-east-1')
    client = Mock()
    client.get_cost_and_usage.side_effect = [
        {'NextPageToken': 'repeat'}, {'NextPageToken': 'repeat'},
        AssertionError('pagination loop continued'),
    ]
    with patch('app.aws.date') as date, patch('app.aws.boto3.client', return_value=client):
        date.today.return_value = __import__('datetime').date(2026, 11, 15)
        with pytest.raises(ValueError, match='pagination'):
            provider.get_monthly_costs()
    assert client.get_cost_and_usage.call_count == 2
