# CloudCost AI ☁️💰

AI-assisted AWS cost optimization API that turns cloud spend and utilization signals into prioritized, explainable savings recommendations.

## Why this project

Cloud bills tell you **what** you spent. CloudCost AI helps explain **where to optimize next**. It combines AWS billing/utilization data with deterministic FinOps rules and an optional Amazon Bedrock explanation layer.

## Features

- AWS Cost Explorer adapter for service-level spend
- CloudWatch-ready utilization model
- Mock mode so the project runs without an AWS account
- FinOps recommendation engine with estimated monthly savings
- Prioritized recommendations with evidence and confidence
- Optional Amazon Bedrock summaries
- FastAPI REST API + automatic OpenAPI docs
- Docker support, unit/API tests, and GitHub Actions CI
- Read-only AWS design: the app recommends changes but never mutates infrastructure

## Architecture

```text
                 ┌─────────────────────┐
                 │      Client/UI      │
                 └──────────┬──────────┘
                            │ HTTP
                    ┌───────▼────────┐
                    │    FastAPI     │
                    └───────┬────────┘
                            │
             ┌──────────────▼──────────────┐
             │     Cost Analysis Service   │
             └──────┬──────────────┬───────┘
                    │              │
          ┌─────────▼──────┐ ┌────▼──────────────┐
          │ AWS Data Layer │ │ Recommendation    │
          │ Cost Explorer  │ │ Engine            │
          │ CloudWatch     │ │ FinOps rules      │
          └─────────┬──────┘ └────┬──────────────┘
                    │              │
                    └──────┬───────┘
                           │
                  ┌────────▼────────┐
                  │ Bedrock (opt.)  │
                  │ AI explanation │
                  └─────────────────┘
```

## Quick start

```bash
git clone https://github.com/AkankshaChoudhary20/cloudcost-ai.git
cd cloudcost-ai

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs`.

Mock mode is enabled by default, so no AWS credentials are required.

## Example

```bash
curl http://localhost:8000/api/v1/analysis
```

Example response:

```json
{
  "monthly_spend": 1240.5,
  "potential_monthly_savings": 226.8,
  "savings_percentage": 18.28,
  "recommendations": [
    {
      "category": "compute",
      "resource_id": "i-0demo123",
      "title": "Rightsize underutilized EC2 instance",
      "estimated_monthly_savings": 96.0,
      "priority": "high"
    }
  ]
}
```

## Real AWS mode

Set `USE_MOCK_DATA=false` and provide AWS credentials using the standard AWS credential chain. The IAM identity should be read-only and allow Cost Explorer access. CloudCost AI intentionally does not terminate, resize, or otherwise modify resources.

## API

| Endpoint | Purpose |
|---|---|
| `GET /health` | Health check |
| `GET /api/v1/costs` | Monthly spend grouped by AWS service |
| `GET /api/v1/recommendations` | Prioritized optimization recommendations |
| `GET /api/v1/analysis` | Combined FinOps analysis |
| `POST /api/v1/explain` | Human-friendly explanation, with optional Bedrock |

## Engineering decisions

**Deterministic recommendations first.** Savings calculations should be auditable, so rules generate recommendations and the LLM only explains them.

**Safe by default.** The service is advisory and read-only.

**Local-first development.** Mock data makes tests and demos deterministic and avoids requiring cloud credentials.

## Roadmap

- EC2 and EBS inventory adapters
- CloudWatch utilization collection
- Savings Plans / Reserved Instance analysis
- Cost anomaly detection
- React/Next.js dashboard
- Historical trend persistence
- Multi-account AWS Organizations support

## Tests

```bash
pytest -q
```

## Docker

```bash
docker build -t cloudcost-ai .
docker run --rm -p 8000:8000 --env-file .env cloudcost-ai
```

## Tech stack

Python · FastAPI · Pydantic · boto3 · Amazon Cost Explorer · Amazon CloudWatch · Amazon Bedrock · Docker · Pytest · GitHub Actions

## Disclaimer

Savings figures are estimates for engineering/demo purposes. Validate pricing, commitments, workload requirements, and operational risk before making production infrastructure changes.
