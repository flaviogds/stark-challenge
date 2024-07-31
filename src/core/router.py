from fastapi import APIRouter

from src.core.invoice import invoice

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(invoice, tags=["Invoice"])
