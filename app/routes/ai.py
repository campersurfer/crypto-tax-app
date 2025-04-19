from fastapi import APIRouter, HTTPException, Request
from termcolor import cprint
from app.services.ai_service import ai_classify_transactions

router = APIRouter()

@router.post("/ai/classify_transactions")
def classify_transactions_api(request: Request):
    try:
        data = await request.json()
        transactions = data.get("transactions", [])
        task_complexity = data.get("task_complexity", "simple")
        cprint(f"[INFO] Received {len(transactions)} transactions for AI classification.", "cyan")
        result = ai_classify_transactions(transactions, task_complexity)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except Exception as e:
        cprint(f"[ERROR] AI classify endpoint failed: {e}", "red")
        raise HTTPException(status_code=500, detail=str(e))
