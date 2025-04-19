from fastapi import APIRouter, Request
from app.services.ai_nft_service import ai_classify_nft_transactions

router = APIRouter()

@router.post("/classify_nft_transactions")
def classify_nft_transactions(request: Request):
    body = await request.json()
    transactions = body.get("transactions", [])
    task_complexity = body.get("task_complexity", "simple")
    result = ai_classify_nft_transactions(transactions, task_complexity)
    return {"results": result}
