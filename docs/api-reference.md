# API Reference

Base URL: `https://aletaindex-narrative.com`

All endpoints (except registration) require:
```
X-API-Key: nk_your_key_here
```

---

## Endpoints

### 1. Comprehensive Narratives
**The main endpoint.** Returns the full narrative hierarchy for one or more tickers.

```
GET /v1/narratives/comprehensive
```

**Parameters**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `tickers` | string | Yes | — | Comma-separated tickers, max 10. e.g. `NVDA,TSLA` |
| `from_date` | date | No | — | Start date `YYYY-MM-DD` |
| `to_date` | date | No | — | End date `YYYY-MM-DD` |
| `days` | int | No | 30 | Lookback days (overridden by from/to_date) |
| `all_time` | bool | No | false | Return full history |
| `article_limit` | int | No | 100 | Max articles per ticker |
| `article_sort_by` | string | No | `representativeness` | `representativeness` or `time` |
| `source` | string | No | — | Filter by news source name |
| `min_relevance` | float | No | — | Min ticker relevance score (0–1) |
| `min_sentiment` | float | No | — | Min sentiment score (-1–1) |
| `max_sentiment` | float | No | — | Max sentiment score (-1–1) |
| `narrative_id` | int | No | — | Filter to a specific narrative |
| `include_aggregation` | bool | No | false | Include sentiment aggregation stats |

**Example**
```bash
curl "https://aletaindex-narrative.com/v1/narratives/comprehensive?tickers=NVDA&days=7" \
  -H "X-API-Key: nk_your_key_here"
```

**Response**
```json
{
  "query": {
    "tickers": ["NVDA"],
    "from_date": "2026-03-09",
    "to_date": "2026-03-16"
  },
  "results": [
    {
      "ticker": "NVDA",
      "timeframe": { "from": "2026-03-09", "to": "2026-03-16" },
      "counts": {
        "global_narrative_count": 5,
        "daily_topic_count": 23,
        "article_count": 187
      },
      "insights": { ... },
      "global_narratives": [
        {
          "id": 42,
          "title": "AI Infrastructure Supercycle",
          "sentiment": { "avg_sentiment": 0.68, "label": "positive" },
          "metadata": { "daily_topic_count": 8, "article_count": 47 },
          "daily_topics": [ ... ]
        }
      ]
    }
  ]
}
```

---

### 2. Global Narratives
Returns the active narratives for a ticker with article samples.

```
GET /v1/narratives/global-narratives
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ticker` | string | Required | Single ticker |
| `days` | int | 30 | Lookback (max 730, null = all time) |
| `limit` | int | 20 | Max narratives (max 100) |
| `include_articles` | bool | true | Include representative articles |

---

### 3. Narrative Timeline
Aggregated sentiment and mention volume over time.

```
GET /v1/narratives/timeline
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ticker` | string | Required | — |
| `days` | int | — | null = all time |

**Returns**: per-date sentiment, article counts, top 5 narratives with daily breakdowns, key events.

---

### 4. Granular Timeline
Sub-daily narrative data at configurable intervals.

```
GET /v1/narratives/timeline-granular
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ticker` | string | Required | — |
| `days` | int | — | — |
| `interval_minutes` | int | 60 | `1`, `15`, `30`, `60`, `240`, `1440` |

---

### 5. LLM Insights
AI-generated analysis: summary, key insights, anomalies, narrative correlations.

```
GET /v1/narratives/insights
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ticker` | string | Required | — |
| `days` | int | 30 | `7`, `30`, `90`, `180`, `365`, or null |

**Returns**: `summary`, `key_insights`, `anomalies`, `correlations`, `behavioral_patterns`

Pre-generated for standard time ranges. Custom ranges generated on-demand.

---

### 6. Summary
Quick counts and recent events for a ticker.

```
GET /v1/narratives/summary
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ticker` | string | Required | — |
| `days` | int | 30 | null = all time |

---

### 7. Daily Topics
Day-level narrative events, filterable by global narrative.

```
GET /v1/narratives/daily-topics
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ticker` | string | Required | — |
| `global_narrative_id` | int | — | Filter to one narrative |
| `from_date` | date | — | — |
| `to_date` | date | — | — |
| `days` | int | 30 | — |
| `limit` | int | 50 | max 200 |
| `include_articles` | bool | true | — |

---

### 8. Price Data
OHLCV price data for a ticker.

```
GET /v1/narratives/price
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ticker` | string | Required | — |
| `days` | int | — | null = all time |
| `interval_minutes` | int | 1 | `1`, `15`, `30`, `60`, `240`, `1440` |

**Returns**: `timestamp_ms`, `datetime_utc`, `open`, `high`, `low`, `close`, `volume`, `daily_return`

---

### 9. Register
Create a new account. Free tier activated immediately.

```
POST /v1/customers/register
```

```json
{
  "customer_name": "Your Name",
  "email": "you@example.com"
}
```

API key delivered by email.

---

## Error Codes

| Code | Meaning |
|------|---------|
| `401` | Missing or invalid API key |
| `403` | Account inactive or expired |
| `429` | Rate limit exceeded (free tier: 100/day) |
| `422` | Invalid parameters |
| `500` | Server error |

---

## Free Tier Limits

| Limit | Value |
|-------|-------|
| Tickers | TSLA only |
| History | Last 1 day |
| Calls/day | 100 |

Upgrade to Pro for full access → [narrative-intelligence.com/register](https://aletaindex-narrative.com/register)
