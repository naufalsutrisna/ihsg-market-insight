from app.services.market_data import (
    get_market_summary,
    get_stock_summaries,
)
from app.services.market_analysis import analyze_market


WATCHLIST = [
    "BBCA.JK",
    "BBRI.JK",
    "BMRI.JK",
    "BBNI.JK",
    "TLKM.JK",
    "ASII.JK",
    "GOTO.JK",
    "AMMN.JK",
    "ADRO.JK",
    "BRPT.JK",
]


def get_closing_insight() -> dict:
    market = get_market_summary()
    stock_result = get_stock_summaries(WATCHLIST)

    stocks = stock_result["data"]

    if not stocks:
        raise ValueError("No stock data available for closing insight")

    analysis = analyze_market(stocks)

    stock_dates = {stock["date"] for stock in stocks}
    all_dates = stock_dates | {market["date"]}

    date_consistent = len(all_dates) == 1
    data_complete = stock_result["total_failed"] == 0

    warnings = []

    if not date_consistent:
        warnings.append("Market and stock data dates are inconsistent")

    if not data_complete:
        warnings.append("Some stock data could not be retrieved")

    if not market["volume_available"]:
        warnings.append("IHSG volume data is unavailable")

    return {
        "report_type": "closing_insight",
        "date": market["date"],
        "source": "yahoo_finance",
        "market": market,
        "analysis": analysis,
        "stock_data": stock_result,
        "data_quality": {
            "date_consistent": date_consistent,
            "stock_data_complete": data_complete,
            "ready_to_publish": date_consistent and data_complete,
            "warnings": warnings,
        },
    }
