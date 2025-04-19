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
    if task_complexity == "simple":
        return random.choice(FREE_MODELS)
    return random.choice(PAID_MODELS)


def ai_analyze_lp_transactions(lp_transactions, task_complexity="simple"):
    if not OPENROUTER_API_KEY:
        cprint("[ERROR] OPENROUTER_API_KEY not set.", "red")
        return {"error": "API key not set."}
    model = select_model(task_complexity)
    prompt = (
        "Analyze the following DeFi liquidity pool (LP) transactions. For each, classify the action (add/remove liquidity, swap, farm, stake, borrow, lend, etc.), identify tokens involved, and summarize the tax implications. Return a JSON list with 'action', 'tokens', and 'tax_summary' for each transaction. Transactions: "
        + str(lp_transactions)
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
        cprint(f"[INFO] Sending LP analysis request to OpenRouter with model: {model}", "cyan")
        resp = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        return result
    except Exception as e:
        cprint(f"[ERROR] AI LP analysis failed: {e}", "red")
        return {"error": str(e)}
