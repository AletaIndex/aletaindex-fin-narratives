"""AletaIndex MCP server — financial narrative intelligence for AI agents."""

import os
import re
from datetime import date, timedelta
from typing import Optional

import httpx
from mcp.server.fastmcp import FastMCP

BASE_URL = "https://aletaindex-narrative.com"

mcp = FastMCP("AletaIndex Narrative Intelligence")


# ── Validation helpers ──────────────────────────────────────────────────────

def _validate_tickers(tickers: str) -> str:
    parts = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    if not parts:
        raise ValueError("At least one ticker is required.")
    if len(parts) > 10:
        raise ValueError(f"Maximum 10 tickers per request (got {len(parts)}).")
    for t in parts:
        if not re.match(r'^[A-Z]{1,5}$', t):
            raise ValueError(
                f"Invalid ticker '{t}'. Use uppercase letters only, e.g. 'NVDA' or 'NVDA,TSLA'."
            )
    return ",".join(parts)


def _validate_date(value: Optional[str], name: str) -> Optional[str]:
    if value is None:
        return None
    try:
        date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"Invalid {name}: '{value}'. Use YYYY-MM-DD format, e.g. '2026-01-15'.")
    return value


def _parse_holdings(holdings: str) -> list:
    result = []
    for item in holdings.split(","):
        item = item.strip()
        if not item:
            continue
        parts = item.split(":")
        if len(parts) != 2:
            raise ValueError(
                f"Invalid holding '{item}'. Use TICKER:WEIGHT format, e.g. 'NVDA:0.30'."
            )
        ticker = parts[0].strip().upper()
        if not re.match(r'^[A-Z]{1,5}$', ticker):
            raise ValueError(f"Invalid ticker '{ticker}' in holdings.")
        try:
            weight = float(parts[1].strip())
        except ValueError:
            raise ValueError(f"Invalid weight for {ticker}: '{parts[1]}'. Use a decimal, e.g. 0.30.")
        if not (0 < weight <= 1):
            raise ValueError(f"Weight for {ticker} must be between 0 and 1 (got {weight}).")
        result.append({"ticker": ticker, "weight": weight})
    if not result:
        raise ValueError("At least one holding is required, e.g. 'NVDA:0.30,AAPL:0.70'.")
    if len(result) > 50:
        raise ValueError(f"Maximum 50 holdings per request (got {len(result)}).")
    return result


# ── HTTP helpers ────────────────────────────────────────────────────────────

def _raise_api_error(e: httpx.HTTPStatusError) -> None:
    status = e.response.status_code
    try:
        detail = e.response.json().get("detail", "")
    except Exception:
        detail = ""
    if status == 401:
        raise ValueError(
            "Invalid API key. Check your NARRATIVE_API_KEY environment variable. "
            "Get a key at https://aletaindex-narrative.com."
        )
    if status == 403:
        msg = f"Access denied: {detail}." if detail else "Access denied."
        raise ValueError(f"{msg} Upgrade at https://aletaindex-narrative.com/subscription.")
    if status == 429:
        raise ValueError("Rate limit exceeded. Please wait a moment before retrying.")
    if status == 422:
        raise ValueError(f"Invalid request: {detail or 'check your parameters.'}")
    raise ValueError(f"API error ({status}): {detail or 'please try again later.'}")


def _get(path: str, params: dict) -> dict:
    api_key = os.environ.get("NARRATIVE_API_KEY", "")
    if not api_key:
        raise ValueError(
            "NARRATIVE_API_KEY is not set. "
            "Get a key at https://aletaindex-narrative.com and set it in your environment."
        )
    params = {k: v for k, v in params.items() if v is not None}
    try:
        r = httpx.get(
            f"{BASE_URL}{path}",
            headers={"X-API-Key": api_key},
            params=params,
            timeout=30,
        )
        r.raise_for_status()
        return r.json()
    except httpx.HTTPStatusError as e:
        _raise_api_error(e)
    except httpx.TimeoutException:
        raise ValueError("Request timed out after 30 seconds. Please try again.")
    except httpx.ConnectError:
        raise ValueError("Could not connect to AletaIndex API. Check your internet connection.")




def _post(path: str, body: dict) -> dict:
    api_key = os.environ.get("NARRATIVE_API_KEY", "")
    if not api_key:
        raise ValueError(
            "NARRATIVE_API_KEY is not set. "
            "Get a key at https://aletaindex-narrative.com and set it in your environment."
        )
    try:
        r = httpx.post(
            f"{BASE_URL}{path}",
            headers={"X-API-Key": api_key, "Content-Type": "application/json"},
            json=body,
            timeout=60,
        )
        r.raise_for_status()
        return r.json()
    except httpx.HTTPStatusError as e:
        _raise_api_error(e)
    except httpx.TimeoutException:
        raise ValueError("Request timed out. Portfolio analysis can take up to 60 seconds.")
    except httpx.ConnectError:
        raise ValueError("Could not connect to AletaIndex API. Check your internet connection.")


# ── MCP tools ───────────────────────────────────────────────────────────────

@mcp.tool()
def get_narratives(
    tickers: str,
    from_date: str = None,
    to_date: str = None,
) -> dict:
    """Get financial narrative intelligence for one or more stocks.

    Returns structured narrative data: persistent story threads (global narratives),
    daily article clusters, individual articles, and sentiment scores. Use this to
    understand what stories are driving a stock and how sentiment is evolving.

    Args:
        tickers: Comma-separated ticker symbols. Examples: "NVDA" or "NVDA,TSLA,AAPL".
                 Maximum 10 tickers per request. Free tier: TSLA, NVDA, AAPL, MSFT,
                 AMZN, GOOGL, META, AMD, NFLX, JPM. Plus/Scale: all 109 tickers.
        from_date: Start date in YYYY-MM-DD format. Defaults to 7 days ago.
        to_date: End date in YYYY-MM-DD format. Defaults to today.

    Returns:
        Dict with narrative data per ticker, including global_narratives (persistent story
        threads with title, sentiment, and dominance), daily_topics (day-level article
        clusters), and articles (individual news items with relevance and sentiment scores).
    """
    tickers = _validate_tickers(tickers)
    from_date = _validate_date(from_date, "from_date")
    to_date = _validate_date(to_date, "to_date")

    if from_date is None:
        from_date = (date.today() - timedelta(days=7)).isoformat()
    if to_date is None:
        to_date = date.today().isoformat()

    return _get("/v1/narratives/comprehensive", {
        "tickers": tickers,
        "from_date": from_date,
        "to_date": to_date,
    })


@mcp.tool()
def get_portfolio_risk(holdings: str) -> dict:
    """Analyze narrative risk across a portfolio of stocks.

    Groups narratives across all holdings by macro theme (e.g. "AI Regulation",
    "Interest Rate Sensitivity") and identifies which stories create concentrated
    narrative exposure across multiple positions simultaneously.

    Args:
        holdings: Portfolio positions as TICKER:WEIGHT pairs, comma-separated.
                  Weights represent portfolio allocation (should sum to ~1.0).
                  Example: "NVDA:0.30,AAPL:0.25,TSLA:0.20,MSFT:0.25"
                  Maximum 50 holdings.

    Returns:
        Dict with macro risk themes, each showing affected tickers, dominant narrative
        titles, sentiment trajectory, and weighted exposure score. Also includes an
        overall portfolio narrative concentration score.
    """
    parsed = _parse_holdings(holdings)
    return _post("/v1/portfolio/narrative-risk", {"holdings": parsed})


if __name__ == "__main__":
    mcp.run()
