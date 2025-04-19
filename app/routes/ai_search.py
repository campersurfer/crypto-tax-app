from fastapi import APIRouter, Request
from app.services.ai_search_service import ai_search_transactions

router = APIRouter()

@router.post("/search_transactions")
async def search_transactions(request: Request):
    body = await request.json()
    transactions = body.get("transactions", [])
    query = body.get("query", "")
    result = ai_search_transactions(transactions, query)
    return {"results": result}
