def format_closing_insight(report: dict) -> str:
    market = report["market"]
    analysis = report["analysis"]
    breadth = analysis["market_breadth"]

    direction = "▲" if market["change"] >= 0 else "▼"
    sign = "+" if market["change"] >= 0 else ""

    lines = [
        f"**IHSG CLOSING INSIGHT — {report['date']}**",
        "",
        "**IHSG Performance**",
        (
            f"{direction} **{market['close']:,.2f}** "
            f"({sign}{market['change_percent']:.2f}%)"
        ),
        f"Open: {market['open']:,.2f}",
        f"High: {market['high']:,.2f}",
        f"Low: {market['low']:,.2f}",
        "",
        "**Market Breadth (Watchlist)**",
        f"Advancing: {breadth['advancing']}",
        f"Declining: {breadth['declining']}",
        f"Unchanged: {breadth['unchanged']}",
        "",
        "**Top Gainers (Watchlist)**",
    ]

    for stock in analysis["top_gainers"]:
        lines.append(
            f"• {stock['symbol']}: +{stock['change_percent']:.2f}%"
        )

    lines.extend(["", "**Top Losers (Watchlist)**"])

    for stock in analysis["top_losers"]:
        lines.append(
            f"• {stock['symbol']}: {stock['change_percent']:.2f}%"
        )

    lines.extend(["", "**Volume Leaders (Watchlist)**"])

    for stock in analysis["volume_leaders"]:
        volume = stock["volume"] / 1_000_000
        lines.append(
            f"• {stock['symbol']}: {volume:,.2f}M shares"
        )

    lines.extend([
        "",
        f"Data source: {report['source']}",
    ])

    warnings = report["data_quality"]["warnings"]

    if warnings:
        lines.extend([
            "",
            "**Data Warnings**",
        ])
        for warning in warnings:
            lines.append(f"• {warning}")

    return "\n".join(lines)
