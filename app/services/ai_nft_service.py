import os
from termcolor import cprint
import requests

def ai_classify_nft_transactions(transactions, task_complexity="simple"):
    """
    Classifies NFT-related transactions using OpenRouter API.
    Returns a list of dicts with NFT action, collection, type, and explanation.
    """
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    if not OPENROUTER_API_KEY:
        cprint("[ERROR] OPENROUTER_API_KEY not set.", "red")
        return [{"error": "No API key set"}]
    prompt = (
        "You are an expert NFT analyst. For each transaction, classify if it is NFT-related (mint, transfer, sale, listing, burn, etc.), "
        "identify the NFT collection (if possible), NFT type (ERC-721, ERC-1155, Solana NFT, etc.), and provide a short explanation. "
        "Format your output as a JSON list of objects with keys: action, collection, type, explanation."
    )
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Classify these transactions: {transactions}"}
    ]
    try:
        cprint("[INFO] Requesting NFT classification via OpenRouter API...", "cyan")
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
                "temperature": 0.4
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
        cprint(f"[ERROR] NFT classification failed: {e}", "red")
        return [{"error": str(e)}]
