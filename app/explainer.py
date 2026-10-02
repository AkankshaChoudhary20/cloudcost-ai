import json
import boto3
from app.config import get_settings
from app.models import AnalysisResponse

def explain_analysis(analysis: AnalysisResponse) -> tuple[str, str]:
    settings = get_settings()
    fallback = (
        f"Current monthly spend is ${analysis.monthly_spend:,.2f}. "
        f"CloudCost AI identified approximately ${analysis.potential_monthly_savings:,.2f} "
        f"({analysis.savings_percentage:.2f}%) in potential monthly savings across "
        f"{len(analysis.recommendations)} recommendations. Review high-priority compute "
        "recommendations first, then validate storage lifecycle and capacity changes."
    )
    if not settings.enable_bedrock:
        return fallback, "deterministic"

    client = boto3.client("bedrock-runtime", region_name=settings.aws_region)
    prompt = (
        "You are an AWS FinOps assistant. Explain this analysis concisely. "
        "Do not invent savings or claim changes were applied. Data: "
        + analysis.model_dump_json()
    )
    try:
        response = client.converse(
            modelId=settings.bedrock_model_id,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"maxTokens": 350, "temperature": 0.2},
        )
        return response["output"]["message"]["content"][0]["text"], "amazon-bedrock"
    except Exception:
        return fallback, "deterministic-fallback"
