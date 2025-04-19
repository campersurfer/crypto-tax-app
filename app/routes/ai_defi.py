from fastapi import APIRouter, Request
from app.services.ai_defi_service import ai_classify_defi_protocols

router = APIRouter()

@router.post("/classify_defi_protocols")
async def classify_defi_protocols(request: Request):
    body = await request.json()
    transactions = body.get("transactions", [])
    result = ai_classify_defi_protocols(transactions)
    return {"results": result}
