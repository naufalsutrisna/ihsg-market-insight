def analyze_market(stocks: list[dict]) -> dict:
    if not stocks:
        raise ValueError("No stock data available for analysis")

    gainers = sorted(
        [stock for stock in stocks if stock["change_percent"] > 0],
        key=lambda stock: stock["change_percent"],
        reverse=True,
    )

    losers = sorted(
        [stock for stock in stocks if stock["change_percent"] < 0],
        key=lambda stock: stock["change_percent"],
    )

    volume_leaders = sorted(
        [stock for stock in stocks if stock["volume_available"]],
        key=lambda stock: stock["volume"],
        reverse=True,
    )

    unchanged = [
        stock for stock in stocks
        if stock["change_percent"] == 0
    ]

    return {
        "market_breadth": {
            "advancing": len(gainers),
            "declining": len(losers),
            "unchanged": len(unchanged),
            "total": len(stocks),
        },
        "top_gainers": gainers[:5],
        "top_losers": losers[:5],
        "volume_leaders": volume_leaders[:5],
    }
