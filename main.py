from fastapi import FastAPI
from termcolor import cprint
from app.routes.health import router as health_router
from app.routes.auth import router as auth_router
from app.routes.wallet import router as wallet_router
from app.routes.exchange import router as exchange_router
from app.routes.transactions import router as transactions_router
from app.routes.classification import router as classification_router
from app.routes.manual_edit import router as manual_edit_router
from app.routes.audit import router as audit_router
from app.routes.tax import router as tax_router
from app.routes.report import router as report_router
from app.routes.lp import router as lp_router
from app.routes.ai import router as ai_router
from app.routes.lp_ai import router as lp_ai_router
from app.routes.ai_nft import router as ai_nft_router

app = FastAPI()

# Register API routers
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(wallet_router, prefix="/wallet")
app.include_router(exchange_router)
app.include_router(transactions_router)
app.include_router(classification_router)
app.include_router(manual_edit_router)
app.include_router(audit_router)
app.include_router(tax_router)
app.include_router(report_router)
app.include_router(lp_router, prefix="/lp")
app.include_router(ai_router, prefix="/ai")
app.include_router(ai_nft_router, prefix="/ai")
app.include_router(ai_tax_router, prefix="/ai")
app.include_router(ai_search_router, prefix="/ai")
app.include_router(ai_defi_router, prefix="/ai")
app.include_router(lp_ai_router, prefix="/lp/ai")

cprint("[INFO] Crypto Tax App FastAPI server initialized.", "cyan")
