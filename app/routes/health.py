from fastapi import APIRouter
from termcolor import cprint

router = APIRouter()

@router.get("/health")
def health_check():
    cprint("Health check endpoint hit.", "green")
    return {"status": "ok"}
