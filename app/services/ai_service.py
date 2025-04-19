import os
import random
import requests
from termcolor import cprint

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

FREE_MODELS = [
    "deepseek-chat",
    "gemini-pro",
]
PAID_MODELS = [
    "gpt-4o",
    "claude-3-opus",
]
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def select_model(task_complexity: str = "simple") -> str:
    """Selects a model based on task complexity and shuffles free models if needed."""
    if task_complexity == "simple":
        model = random.choice(FREE_MODELS)
    else:
        model = random.choice(PAID_MODELS)
    return model


def ai_classify_transactions(transactions, task_complexity="simple"):
    """Call OpenRouter API for transaction classification, prioritizing free models."""
    if not OPENROUTER_API_KEY:
        cprint("[ERROR] OPENROUTER_API_KEY not set.", "red")
        return {"error": "API key not set."}
    model = select_model(task_complexity)
    prompt = (
        "Classify the following crypto transactions by type (trade, staking, LP, NFT, airdrop, etc.) and return a JSON list with a 'type' and 'explanation' for each transaction. "
        "Transactions: " + str(transactions)
    )
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    try:
        cprint(f"[INFO] Sending classification request to OpenRouter with model: {model}", "cyan")
        resp = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        return result
    except Exception as e:
        cprint(f"[ERROR] AI classification failed: {e}", "red")
        return {"error": str(e)}
