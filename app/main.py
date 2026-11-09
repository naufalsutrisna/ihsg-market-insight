from fastapi import FastAPI

from app.routers.market import router as market_router


app = FastAPI(
    title="IHSG Market Insight API",
    description="Indonesian stock market data and insights.",
    version="0.1.0",
)


app.include_router(market_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
