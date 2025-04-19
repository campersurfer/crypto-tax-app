import os
import requests
import random
from termcolor import cprint

def fetch_wallet_transactions(address: str, chain: str = "eth"):
    """
    Fetch transactions for a wallet address on ETH, Base, Arbitrum, Solana, or Bitcoin.
    - EVM chains (ETH, BASE, ARB): Covalent API
    - Solana: Helius API
    - Bitcoin: Blockstream API
    Falls back to mock data if no API key or on error.
    """
    chain = chain.lower()
    if chain in ["eth", "ethereum", "base", "arbitrum", "arb"]:
        return _fetch_evm_transactions(address, chain)
    elif chain == "sol" or chain == "solana":
        return _fetch_solana_transactions(address)
    elif chain == "btc" or chain == "bitcoin":
        return _fetch_bitcoin_transactions(address)
    else:
        cprint(f"[WARN] Unsupported chain '{chain}', using mock data.", "yellow")
        return _mock_transactions(address)


def _fetch_evm_transactions(address: str, chain: str):
    COVALENT_API_KEY = os.getenv("COVALENT_API_KEY")
    if not COVALENT_API_KEY:
        cprint("[WARN] COVALENT_API_KEY not set, using mock data.", "yellow")
        return _mock_transactions(address)
    chain_ids = {"eth": "1", "ethereum": "1", "base": "8453", "arbitrum": "42161", "arb": "42161"}
    chain_id = chain_ids.get(chain, "1")
    url = f"https://api.covalenthq.com/v1/{chain_id}/address/{address}/transactions_v2/?key={COVALENT_API_KEY}"
    cprint(f"[INFO] Fetching transactions for {address} on {chain} via Covalent API", "cyan")
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        txs = []
        for tx in data.get("data", {}).get("items", []):
            txs.append({
                "id": tx.get("tx_hash"),
                "from": tx.get("from_address"),
                "to": tx.get("to_address"),
                "amount": tx.get("value"),
                "token": tx.get("contract_ticker_symbol", "ETH"),
                "type": "transfer"
            })
        if not txs:
            cprint("[WARN] No transactions found from Covalent, using mock data.", "yellow")
            return _mock_transactions(address)
        return txs
    except Exception as e:
        cprint(f"[ERROR] Covalent API failed: {e}. Using mock data.", "red")
        return _mock_transactions(address)


def _fetch_solana_transactions(address: str):
    HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
    if not HELIUS_API_KEY:
        cprint("[WARN] HELIUS_API_KEY not set, using mock data.", "yellow")
        return _mock_transactions(address)
    url = f"https://api.helius.xyz/v0/addresses/{address}/transactions?api-key={HELIUS_API_KEY}"
    cprint(f"[INFO] Fetching Solana transactions for {address} via Helius API", "cyan")
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        txs = []
        for tx in data:
            txs.append({
                "id": tx.get("signature"),
                "from": tx.get("accountData", [{}])[0].get("account", ""),
                "to": tx.get("accountData", [{}])[-1].get("account", ""),
                "amount": tx.get("amount", ""),
                "token": tx.get("token", "SOL"),
                "type": tx.get("type", "transfer")
            })
        if not txs:
            cprint("[WARN] No transactions found from Helius, using mock data.", "yellow")
            return _mock_transactions(address)
        return txs
    except Exception as e:
        cprint(f"[ERROR] Helius API failed: {e}. Using mock data.", "red")
        return _mock_transactions(address)


def _fetch_bitcoin_transactions(address: str):
    # Blockstream API is public, no key needed
    url = f"https://blockstream.info/api/address/{address}/txs"
    cprint(f"[INFO] Fetching Bitcoin transactions for {address} via Blockstream API", "cyan")
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        txs = []
        for tx in data:
            txs.append({
                "id": tx.get("txid"),
                "from": tx.get("vin", [{}])[0].get("prevout", {}).get("scriptpubkey_address", ""),
                "to": tx.get("vout", [{}])[0].get("scriptpubkey_address", ""),
                "amount": tx.get("vout", [{}])[0].get("value", 0) / 1e8,
                "token": "BTC",
                "type": "transfer"
            })
        if not txs:
            cprint("[WARN] No transactions found from Blockstream, using mock data.", "yellow")
            return _mock_transactions(address)
        return txs
    except Exception as e:
        cprint(f"[ERROR] Blockstream API failed: {e}. Using mock data.", "red")
        return _mock_transactions(address)

def _mock_transactions(address: str):
    return [
        {"id": f"tx_{random.randint(1000,9999)}", "from": address, "to": "0xabc...", "amount": 1.23, "token": "ETH", "type": "transfer"},
        {"id": f"tx_{random.randint(1000,9999)}", "from": address, "to": "0xdef...", "amount": 0.5, "token": "USDC", "type": "swap"},
    ]
