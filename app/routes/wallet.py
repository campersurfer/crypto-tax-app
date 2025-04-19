from fastapi import APIRouter, HTTPException
from termcolor import cprint

router = APIRouter()

@router.post("/wallet/import")
def import_wallet(address: str, chain: str):
    try:
        cprint(f"[INFO] Importing wallet {address} on {chain}.", "cyan")
        # Placeholder: Implement wallet import logic for all major chains
        return {"message": f"Wallet {address} imported for {chain} (to be implemented)"}
    except Exception as e:
        cprint(f"[ERROR] {str(e)}", "red")
        raise HTTPException(status_code=500, detail="Wallet import failed.")

@router.post("/wallet/fetch_transactions")
def fetch_transactions(address: str, chain: str = "eth"):
    try:
        from app.utils.fetch_wallet_transactions import fetch_wallet_transactions
        cprint(f"[INFO] Fetching transactions for {address} on {chain}.", "cyan")
        txs = fetch_wallet_transactions(address, chain)
        return {"transactions": txs}
    except Exception as e:
        cprint(f"[ERROR] {str(e)}", "red")
        raise HTTPException(status_code=500, detail="Fetch transactions failed.")
