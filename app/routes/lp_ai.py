from fastapi import APIRouter, HTTPException, Request
from termcolor import cprint
from app.services.ai_lp_service import ai_analyze_lp_transactions

router = APIRouter()

@router.post("/ai/analyze_lp")
async def analyze_lp_api(request: Request):
    try:
        data = await request.json()
        lp_transactions = data.get("lp_transactions", [])
        task_complexity = data.get("task_complexity", "simple")
        cprint(f"[INFO] Received {len(lp_transactions)} LP transactions for AI analysis.", "cyan")
        result = ai_analyze_lp_transactions(lp_transactions, task_complexity)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except Exception as e:
        cprint(f"[ERROR] AI LP analysis endpoint failed: {e}", "red")
        raise HTTPException(status_code=500, detail=str(e))
