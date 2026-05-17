"""Tests for AletaIndex MCP server — validation, error handling, and API calls."""

import os
import sys
import pytest
import respx
import httpx

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from server import (
    _validate_tickers,
    _validate_date,
    _parse_holdings,
    _raise_api_error,
    get_narratives,
    get_portfolio_risk,
)

BASE = "https://aletaindex-narrative.com"
TEST_KEY = "nk_test_key_abc123"


# ── _validate_tickers ────────────────────────────────────────────────────────

class TestValidateTickers:
    def test_single(self):
        assert _validate_tickers("NVDA") == "NVDA"

    def test_multiple(self):
        assert _validate_tickers("NVDA,TSLA,AAPL") == "NVDA,TSLA,AAPL"

    def test_lowercase_normalized(self):
        assert _validate_tickers("nvda,tsla") == "NVDA,TSLA"

    def test_whitespace_stripped(self):
        assert _validate_tickers("NVDA, TSLA , AAPL") == "NVDA,TSLA,AAPL"

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="At least one ticker"):
            _validate_tickers("")

    def test_too_many_raises(self):
        with pytest.raises(ValueError, match="Maximum 10"):
            _validate_tickers("A,B,C,D,E,F,G,H,I,J,K")

    def test_numbers_in_ticker_raises(self):
        with pytest.raises(ValueError, match="Invalid ticker"):
            _validate_tickers("NVDA123")

    def test_injection_rejected(self):
        with pytest.raises(ValueError, match="Invalid ticker"):
            _validate_tickers("NVDA; DROP TABLE")

    def test_special_chars_rejected(self):
        with pytest.raises(ValueError, match="Invalid ticker"):
            _validate_tickers("NV DA")


# ── _validate_date ────────────────────────────────────────────────────────────

class TestValidateDate:
    def test_valid(self):
        assert _validate_date("2026-01-15", "from_date") == "2026-01-15"

    def test_none_passthrough(self):
        assert _validate_date(None, "from_date") is None

    def test_wrong_order_raises(self):
        with pytest.raises(ValueError, match="Invalid from_date"):
            _validate_date("15-01-2026", "from_date")

    def test_invalid_month_raises(self):
        with pytest.raises(ValueError, match="Invalid from_date"):
            _validate_date("2026-13-01", "from_date")

    def test_invalid_format_raises(self):
        with pytest.raises(ValueError, match="Invalid to_date"):
            _validate_date("not-a-date", "to_date")


# ── _parse_holdings ───────────────────────────────────────────────────────────

class TestParseHoldings:
    def test_valid(self):
        result = _parse_holdings("NVDA:0.30,AAPL:0.70")
        assert result == [
            {"ticker": "NVDA", "weight": 0.30},
            {"ticker": "AAPL", "weight": 0.70},
        ]

    def test_lowercase_normalized(self):
        result = _parse_holdings("nvda:0.5,tsla:0.5")
        assert result[0]["ticker"] == "NVDA"

    def test_whitespace_stripped(self):
        result = _parse_holdings("NVDA : 0.5 , AAPL : 0.5")
        assert result[0]["ticker"] == "NVDA"

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="At least one"):
            _parse_holdings("")

    def test_missing_colon_raises(self):
        with pytest.raises(ValueError, match="Invalid holding"):
            _parse_holdings("NVDA-0.30")

    def test_non_numeric_weight_raises(self):
        with pytest.raises(ValueError, match="Invalid weight"):
            _parse_holdings("NVDA:abc")

    def test_weight_above_one_raises(self):
        with pytest.raises(ValueError, match="between 0 and 1"):
            _parse_holdings("NVDA:1.5")

    def test_zero_weight_raises(self):
        with pytest.raises(ValueError, match="between 0 and 1"):
            _parse_holdings("NVDA:0")

    def test_too_many_holdings_raises(self):
        # Use valid single-letter tickers to hit the count check
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        tickers = [letters[i % 26] * (i // 26 + 1) for i in range(51)]
        holdings = ",".join(f"{t[:5]}:{0.02}" for t in tickers)
        with pytest.raises(ValueError, match="Maximum 50"):
            _parse_holdings(holdings)


# ── _raise_api_error ──────────────────────────────────────────────────────────

class TestRaiseApiError:
    def _make_error(self, status: int, detail: str = "") -> httpx.HTTPStatusError:
        body = {"detail": detail} if detail else {}
        response = httpx.Response(status, json=body)
        return httpx.HTTPStatusError("error", request=httpx.Request("GET", BASE), response=response)

    def test_401_friendly(self):
        with pytest.raises(ValueError, match="Invalid API key"):
            _raise_api_error(self._make_error(401))

    def test_403_with_detail(self):
        with pytest.raises(ValueError, match="Access denied"):
            _raise_api_error(self._make_error(403, "Ticker AMZN requires Plus tier"))

    def test_429_friendly(self):
        with pytest.raises(ValueError, match="Rate limit"):
            _raise_api_error(self._make_error(429))

    def test_422_with_detail(self):
        with pytest.raises(ValueError, match="Invalid request"):
            _raise_api_error(self._make_error(422, "field required"))

    def test_500_generic(self):
        with pytest.raises(ValueError, match="API error \\(500\\)"):
            _raise_api_error(self._make_error(500))


# ── get_narratives (HTTP mocked) ──────────────────────────────────────────────

MOCK_NARRATIVES = {"results": [{"ticker": "NVDA", "global_narratives": []}]}


@respx.mock
def test_get_narratives_success(monkeypatch):
    monkeypatch.setenv("NARRATIVE_API_KEY", TEST_KEY)
    respx.get(f"{BASE}/v1/narratives/comprehensive").mock(
        return_value=httpx.Response(200, json=MOCK_NARRATIVES)
    )
    result = get_narratives("NVDA", from_date="2026-05-01", to_date="2026-05-10")
    assert result == MOCK_NARRATIVES


@respx.mock
def test_get_narratives_default_dates(monkeypatch):
    monkeypatch.setenv("NARRATIVE_API_KEY", TEST_KEY)
    route = respx.get(f"{BASE}/v1/narratives/comprehensive").mock(
        return_value=httpx.Response(200, json=MOCK_NARRATIVES)
    )
    get_narratives("NVDA")
    # Verify from_date and to_date were set (not None)
    params = route.calls[0].request.url.params
    assert "from_date" in params
    assert "to_date" in params


@respx.mock
def test_get_narratives_multiple_tickers(monkeypatch):
    monkeypatch.setenv("NARRATIVE_API_KEY", TEST_KEY)
    route = respx.get(f"{BASE}/v1/narratives/comprehensive").mock(
        return_value=httpx.Response(200, json=MOCK_NARRATIVES)
    )
    get_narratives("NVDA,TSLA,AAPL")
    params = route.calls[0].request.url.params
    assert params["tickers"] == "NVDA,TSLA,AAPL"


@respx.mock
def test_get_narratives_401(monkeypatch):
    monkeypatch.setenv("NARRATIVE_API_KEY", TEST_KEY)
    respx.get(f"{BASE}/v1/narratives/comprehensive").mock(
        return_value=httpx.Response(401, json={"detail": "Invalid API key"})
    )
    with pytest.raises(ValueError, match="Invalid API key"):
        get_narratives("NVDA")


@respx.mock
def test_get_narratives_403_ticker_restriction(monkeypatch):
    monkeypatch.setenv("NARRATIVE_API_KEY", TEST_KEY)
    respx.get(f"{BASE}/v1/narratives/comprehensive").mock(
        return_value=httpx.Response(403, json={"detail": "Ticker GS requires Plus tier"})
    )
    with pytest.raises(ValueError, match="Access denied"):
        get_narratives("GS")


@respx.mock
def test_get_narratives_429(monkeypatch):
    monkeypatch.setenv("NARRATIVE_API_KEY", TEST_KEY)
    respx.get(f"{BASE}/v1/narratives/comprehensive").mock(
        return_value=httpx.Response(429, json={})
    )
    with pytest.raises(ValueError, match="Rate limit"):
        get_narratives("NVDA")


def test_get_narratives_no_api_key(monkeypatch):
    monkeypatch.delenv("NARRATIVE_API_KEY", raising=False)
    with pytest.raises(ValueError, match="NARRATIVE_API_KEY is not set"):
        get_narratives("NVDA")


def test_get_narratives_invalid_ticker():
    with pytest.raises(ValueError, match="Invalid ticker"):
        get_narratives("NV DA")


# ── get_portfolio_risk (HTTP mocked) ──────────────────────────────────────────

MOCK_PORTFOLIO = {"themes": [], "concentration_risk": 0.25}


@respx.mock
def test_get_portfolio_risk_success(monkeypatch):
    monkeypatch.setenv("NARRATIVE_API_KEY", TEST_KEY)
    respx.post(f"{BASE}/v1/portfolio/narrative-risk").mock(
        return_value=httpx.Response(200, json=MOCK_PORTFOLIO)
    )
    result = get_portfolio_risk("NVDA:0.50,AAPL:0.50")
    assert result == MOCK_PORTFOLIO


@respx.mock
def test_get_portfolio_risk_sends_correct_body(monkeypatch):
    monkeypatch.setenv("NARRATIVE_API_KEY", TEST_KEY)
    route = respx.post(f"{BASE}/v1/portfolio/narrative-risk").mock(
        return_value=httpx.Response(200, json=MOCK_PORTFOLIO)
    )
    get_portfolio_risk("NVDA:0.30,AAPL:0.70")
    import json
    body = json.loads(route.calls[0].request.content)
    assert body == {
        "holdings": [
            {"ticker": "NVDA", "weight": 0.30},
            {"ticker": "AAPL", "weight": 0.70},
        ]
    }


def test_get_portfolio_risk_invalid_format():
    with pytest.raises(ValueError, match="Invalid holding"):
        get_portfolio_risk("NVDA-0.50,AAPL-0.50")


def test_get_portfolio_risk_no_api_key(monkeypatch):
    monkeypatch.delenv("NARRATIVE_API_KEY", raising=False)
    with pytest.raises(ValueError, match="NARRATIVE_API_KEY is not set"):
        get_portfolio_risk("NVDA:0.5,AAPL:0.5")
