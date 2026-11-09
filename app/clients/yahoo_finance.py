import yfinance as yf


def get_history(
    symbol: str,
    period: str = "5d",
    interval: str = "1d",
):
    ticker = yf.Ticker(symbol)

    history = ticker.history(
        period=period,
        interval=interval,
        auto_adjust=False,
    )

    if history.empty:
        raise ValueError(f"No market data found for {symbol}")

    return history
