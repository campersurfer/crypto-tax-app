import os
from termcolor import cprint
import requests

def ai_search_transactions(transactions, query):
    """
    Uses OpenRouter API to perform natural language search over transactions.
    Returns a list of matching transactions with AI explanations.
    """
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    if not OPENROUTER_API_KEY:
        cprint("[ERROR] OPENROUTER_API_KEY not set.", "red")
        return [{"error": "No API key set"}]
    prompt = (
        "You are a crypto transaction search assistant. Given a user query and a list of transactions, "
        "return only the relevant transactions as a JSON list, each with a brief explanation of why it matches. "
        "If no matches, return an empty list."
    )
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Query: {query}\nTransactions: {transactions}"}
    ]
    try:
        cprint("[INFO] Requesting transaction search via OpenRouter API...", "cyan")
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
        cprint(f"[ERROR] Transaction search failed: {e}", "red")
        return [{"error": str(e)}]
