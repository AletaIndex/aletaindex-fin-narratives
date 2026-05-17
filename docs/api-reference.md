# API Reference

**Base URL:** `https://aletaindex-narrative.com`

All endpoints require an API key in the request header:
```
X-API-Key: nk_your_key_here
```

Get a key at [aletaindex-narrative.com](https://aletaindex-narrative.com).

---

## Endpoints

### 1. Comprehensive Narratives

The main data endpoint. Returns the full narrative hierarchy for one or more tickers: global narratives, daily topic clusters, individual articles, and sentiment scores.

```
GET /v1/narratives/comprehensive
```

**Parameters**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `tickers` | string | Yes | — | Comma-separated tickers, max 10. e.g. `NVDA,TSLA` |
| `from_date` | date | No | 7 days ago | Start date `YYYY-MM-DD` |
| `to_date` | date | No | today | End date `YYYY-MM-DD` |
| `all_time` | bool | No | false | Use full available history (ignores `from_date`) |
| `top_articles_per_daily_topic` | int | No | — | Limit articles per daily topic (e.g. `10`). Use this to reduce response size when you only need representative headlines |
| `article_sort_by` | string | No | `representativeness` | `representativeness` or `time` |
| `source` | string | No | — | Filter articles by source domain (e.g. `reuters.com`) |
| `min_relevance` | float | No | — | Min ticker relevance score `0.0–1.0` |
| `min_sentiment` | float | No | — | Min sentiment score `-1.0–1.0` |
| `max_sentiment` | float | No | — | Max sentiment score `-1.0–1.0` |
| `narrative_id` | int | No | — | Filter to a specific global narrative ID |
| `include_aggregation` | bool | No | false | Include daily sentiment aggregation per ticker |
| `paginate` | bool | No | false | For UI lazy loading only. Returns articles in pages using `article_limit` + `article_offset`. Not needed for standard use — the default returns all articles |
| `article_limit` | int | No | — | Articles per page (max 100). Only used with `paginate=true` |
| `article_offset` | int | No | 0 | Page offset. Only used with `paginate=true` |

**Example**
```bash
curl "https://aletaindex-narrative.com/v1/narratives/comprehensive?tickers=NVDA&from_date=2026-05-01&to_date=2026-05-10" \
  -H "X-API-Key: nk_your_key_here"
```

**Response**
```json
{
  "query_summary": {
    "tickers": ["NVDA"],
    "timeframe": {
      "from_date": "2026-05-01",
      "to_date": "2026-05-10",
      "days": 10
    },
    "requested_at": "2026-05-10T08:00:00+00:00"
  },
  "results": [
    {
      "ticker": "NVDA",
      "timeframe": { "from_date": "2026-05-01", "to_date": "2026-05-10" },
      "summary": {
        "global_narrative_count": 5,
        "daily_topic_count": 23,
        "article_count": 187,
        "source_count": 42
      },
      "global_narratives": [
        {
          "id": 42,
          "title": "AI Infrastructure Supercycle",
          "is_active": true,
          "sentiment": {
            "avg_sentiment": 0.68,
            "label": "positive"
          },
          "metadata": {
            "daily_topic_count": 8,
            "article_count": 47,
            "first_seen": "2026-03-01",
            "last_seen": "2026-05-10"
          },
          "daily_topics": [
            {
              "id": 1024,
              "event_date": "2026-05-10",
              "dominance_score": 0.72,
              "article_count": 12,
              "articles": [
                {
                  "title": "NVIDIA's H100 demand surges as hyperscalers expand AI capacity",
                  "source": "reuters.com",
                  "published_at": "2026-05-10T09:15:00Z",
                  "sentiment_score": 0.74,
                  "ticker_relevance_score": 0.92
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

---

### 2. Portfolio Narrative Risk

Analyzes narrative risk across a portfolio. Groups narratives by macro theme and identifies which stories create concentrated exposure across multiple holdings simultaneously.

```
POST /v1/portfolio/narrative-risk
```

**Request Body**
```json
{
  "holdings": [
    { "ticker": "NVDA", "weight": 0.30 },
    { "ticker": "AAPL", "weight": 0.25 },
    { "ticker": "TSLA", "weight": 0.20 },
    { "ticker": "MSFT", "weight": 0.25 }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `holdings` | array | Portfolio positions. Max 50. |
| `holdings[].ticker` | string | Ticker symbol |
| `holdings[].weight` | float | Portfolio allocation fraction (0–1, should sum to ~1.0) |

**Example**
```bash
curl -X POST "https://aletaindex-narrative.com/v1/portfolio/narrative-risk" \
  -H "X-API-Key: nk_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"holdings": [{"ticker": "NVDA", "weight": 0.5}, {"ticker": "AAPL", "weight": 0.5}]}'
```

**Response**
```json
{
  "narratives": [
    {
      "theme": "AI Infrastructure & Compute",
      "tickers": ["NVDA", "MSFT"],
      "exposure_pct": 0.55,
      "dominance": 0.72,
      "trajectory": "ESCALATING",
      "momentum_delta": 0.08,
      "narrative_ids": [42, 17],
      "ticker_narratives": {
        "NVDA": [{ "id": 42, "title": "AI Infrastructure Supercycle" }],
        "MSFT": [{ "id": 17, "title": "Azure AI Buildout" }]
      }
    }
  ],
  "top_risk": "AI Infrastructure & Compute",
  "uncovered_tickers": [],
  "credits_used": 8
}
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| `401` | Missing or invalid API key |
| `403` | Ticker or feature requires Plus/Scale tier |
| `422` | Invalid parameters |
| `429` | Rate limit exceeded |
| `500` | Server error |

---

## Tier Limits

| Tier | Tickers | History | Credits |
|------|---------|---------|---------|
| **Free Trial** | 10 (TSLA, NVDA, AAPL, MSFT, AMZN, GOOGL, META, AMD, NFLX, JPM) | 90 days | 500 total |
| **Plus** | All 109 | 180 days | 2,500/month |
| **Scale** | All 109 | Full history | Unlimited |

Credits are consumed per ticker per day queried via `/v1/narratives/comprehensive` and `/v1/portfolio/narrative-risk`.

[→ Upgrade at aletaindex-narrative.com/subscription](https://aletaindex-narrative.com/subscription)
