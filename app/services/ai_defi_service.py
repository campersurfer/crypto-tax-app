import os
from termcolor import cprint
import requests

def ai_classify_defi_protocols(transactions):
    """
    Uses OpenRouter API to classify DeFi protocol and action for each transaction.
    Returns a list of dicts with protocol, action, and explanation.
    """
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    if not OPENROUTER_API_KEY:
        cprint("[ERROR] OPENROUTER_API_KEY not set.", "red")
        return [{"error": "No API key set"}]
    prompt = (
        "You are a DeFi protocol classification assistant. For each transaction, identify the DeFi protocol (e.g., Uniswap, Aave, Compound, Lido, etc.), "
        "the action (swap, deposit, borrow, stake, etc.), and provide a brief explanation. "
        "Output a JSON list of objects with keys: protocol, action, explanation."
    )
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Classify these transactions: {transactions}"}
    ]
    try:
        cprint("[INFO] Requesting DeFi protocol classification via OpenRouter API...", "cyan")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o",
                "messages": messages,
                "max_tokens": 1024,
                "temperature": 0.3
            },
            timeout=30
        )
        response.raise_for_status()
        answer = response.json()["choices"][0]["message"]["content"]
        import json
        try:
            result = json.loads(answer)
        except Exception:
            result = [{"error": "AI response not valid JSON", "raw": answer}]
        return result
    except Exception as e:
        cprint(f"[ERROR] DeFi protocol classification failed: {e}", "red")
        return [{"error": str(e)}]
