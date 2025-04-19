from fastapi import APIRouter, Request
from app.services.ai_tax_service import ai_generate_tax_summary

router = APIRouter()

@router.post("/tax_report_summary")
async def tax_report_summary(request: Request):
    body = await request.json()
    transactions = body.get("transactions", [])
    breakdown_by_chain = body.get("breakdown_by_chain", False)
    breakdown_by_asset = body.get("breakdown_by_asset", False)
    result = ai_generate_tax_summary(transactions, breakdown_by_chain, breakdown_by_asset)
    return result
