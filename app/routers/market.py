from fastapi import APIRouter, HTTPException

from app.services.market_data import get_market_summary
from app.services.report import get_closing_insight
from app.services.discord_formatter import format_closing_insight


router = APIRouter(
    prefix="/market",
    tags=["Market"],
)


@router.get("/summary")
def market_summary():
    try:
        return get_market_summary()
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        )


@router.get("/closing-insight")
def closing_insight():
    try:
        return get_closing_insight()
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        )


@router.get("/closing-insight/discord")
def closing_insight_discord():
    try:
        report = get_closing_insight()
        return {
            "report_type": "closing_insight",
            "date": report["date"],
            "message": format_closing_insight(report),
            "ready_to_publish": report["data_quality"]["ready_to_publish"],
            "warnings": report["data_quality"]["warnings"],
        }
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        )
