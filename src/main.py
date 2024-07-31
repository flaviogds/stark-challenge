from fastapi import FastAPI

from src.core.router import api_router

app = FastAPI(title="StarkChallenge", description="Stark Bank Skills Test", version="0.1.0", docs_url="/api/docs")

app.include_router(api_router)
