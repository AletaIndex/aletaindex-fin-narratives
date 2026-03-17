import os
import httpx
from mcp.server.fastmcp import FastMCP

API_KEY = os.environ.get("NARRATIVE_API_KEY", "")
BASE_URL = "https://aletaindex-narrative.com"

mcp = FastMCP("Narrative Intelligence")


def _get(path: str, params: dict) -> dict:
    params = {k: v for k, v in params.items() if v is not None}
    r = httpx.get(f"{BASE_URL}{path}", headers={"X-API-Key": API_KEY}, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


@mcp.tool()
def get_narratives(ticker: str, days: int = 7) -> dict:
    """Get the full narrative hierarchy for a ticker: global narratives, daily topics, and articles with sentiment scores."""
    return _get("/v1/narratives/comprehensive", {"tickers": ticker, "days": days})


@mcp.tool()
def get_insights(ticker: str, days: int = 30) -> dict:
    """Get LLM-generated narrative insights for a ticker: summary, key insights, anomalies, and correlations."""
    return _get("/v1/narratives/insights", {"ticker": ticker, "days": days})


@mcp.tool()
def get_timeline(ticker: str, days: int = 30) -> dict:
    """Get sentiment and mention volume over time for a ticker. Useful for spotting narrative momentum shifts."""
    return _get("/v1/narratives/timeline", {"ticker": ticker, "days": days})


@mcp.tool()
def get_price(ticker: str, days: int = 30) -> dict:
    """Get OHLCV price data with daily returns for a ticker."""
    return _get("/v1/narratives/price", {"ticker": ticker, "days": days, "interval_minutes": 1440})


if __name__ == "__main__":
    mcp.run()
