
from app.clients.yahoo_finance import get_history


def _calculate_price_summary(history, symbol: str) -> dict:
    if len(history) < 2:
        raise ValueError("Insufficient market data")

    latest = history.iloc[-1]
    previous = history.iloc[-2]

    close = float(latest["Close"])
    previous_close = float(previous["Close"])
    volume = int(latest["Volume"])

    if close <= 0 or previous_close <= 0:
        raise ValueError("Invalid stock price")

    change = close - previous_close
    change_percent = (change / previous_close) * 100

    return {
        "symbol": symbol,
        "date": latest.name.strftime("%Y-%m-%d"),
        "close": round(close, 2),
        "previous_close": round(previous_close, 2),
        "change": round(change, 2),
        "change_percent": round(change_percent, 2),
        "volume": volume,
        "volume_available": volume > 0,
    }


def get_market_summary(symbol: str = "^JKSE") -> dict:
    history = get_history(
        symbol=symbol,
        period="5d",
        interval="1d",
    )

    summary = _calculate_price_summary(history, symbol)

    latest = history.iloc[-1]

    summary.update({
        "open": round(float(latest["Open"]), 2),
        "high": round(float(latest["High"]), 2),
        "low": round(float(latest["Low"]), 2),
        "source": "yahoo_finance",
    })

    return summary


def get_stock_summaries(symbols: list[str]) -> dict:
    results = []
    errors = []

    for symbol in symbols:
        try:
            history = get_history(
                symbol=symbol,
                period="5d",
                interval="1d",
            )

            summary = _calculate_price_summary(history, symbol)
            results.append(summary)

        except Exception as error:
            errors.append({
                "symbol": symbol,
                "error": str(error),
            })

    return {
        "data": results,
        "errors": errors,
        "total_requested": len(symbols),
        "total_success": len(results),
        "total_failed": len(errors),
    }
