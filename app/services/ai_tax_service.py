import os
from termcolor import cprint
import requests

def ai_generate_tax_summary(transactions, breakdown_by_chain=False, breakdown_by_asset=False):
    """
    Generates a plain-English tax summary for the given transactions using OpenRouter API.
    Returns a summary string and optionally breakdowns.
    """
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    if not OPENROUTER_API_KEY:
        cprint("[ERROR] OPENROUTER_API_KEY not set.", "red")
        return {"error": "No API key set"}
    prompt = (
        "You are a crypto tax expert. Analyze the following transactions and generate a plain-English summary of the user's tax position. "
        "Include total gains/losses, taxable events, and key actions. "
        + ("Break down by chain. " if breakdown_by_chain else "")
        + ("Break down by asset. " if breakdown_by_asset else "")
        + "Be concise and clear."
    )
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Analyze these transactions: {transactions}"}
    ]
    try:
        cprint("[INFO] Requesting tax summary via OpenRouter API...", "cyan")
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
        return {"summary": answer}
    except Exception as e:
        cprint(f"[ERROR] Tax summary generation failed: {e}", "red")
        return {"error": str(e)}
