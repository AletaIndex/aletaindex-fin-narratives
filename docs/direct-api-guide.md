# Direct API Guide

Use the Narrative Intelligence REST API from any language or framework.

---

## Authentication

All requests require an API key in the header:

```
X-API-Key: nk_your_key_here
```

Get your key at [aletaindex-narrative.com](https://aletaindex-narrative.com).

---

## Python

```python
import requests
from datetime import date, timedelta

API_KEY = "nk_your_key_here"
BASE_URL = "https://aletaindex-narrative.com"

headers = {"X-API-Key": API_KEY}

# Get narratives for NVDA — last 7 days
today = date.today().isoformat()
week_ago = (date.today() - timedelta(days=7)).isoformat()

response = requests.get(
    f"{BASE_URL}/v1/narratives/comprehensive",
    headers=headers,
    params={"tickers": "NVDA", "from_date": week_ago, "to_date": today}
)

data = response.json()

for narrative in data["results"][0]["global_narratives"]:
    print(f"{narrative['title']}: {narrative['sentiment']['avg_sentiment']:.2f}")
```

---

## JavaScript / TypeScript

```typescript
const API_KEY = "nk_your_key_here";
const BASE_URL = "https://aletaindex-narrative.com";

async function getNarratives(ticker: string, fromDate: string, toDate: string) {
  const params = new URLSearchParams({ tickers: ticker, from_date: fromDate, to_date: toDate });
  const response = await fetch(
    `${BASE_URL}/v1/narratives/comprehensive?${params}`,
    { headers: { "X-API-Key": API_KEY } }
  );
  return response.json();
}

const today = new Date().toISOString().split("T")[0];
const weekAgo = new Date(Date.now() - 7 * 86400000).toISOString().split("T")[0];

const data = await getNarratives("NVDA", weekAgo, today);
for (const narrative of data.results[0].global_narratives) {
  console.log(narrative.title, narrative.sentiment.avg_sentiment);
}
```

---

## Common Patterns

### Get all active narratives for a ticker
```python
response = requests.get(
    f"{BASE_URL}/v1/narratives/comprehensive",
    headers=headers,
    params={"tickers": "TSLA", "from_date": "2026-05-01", "to_date": "2026-05-10"}
)
for narrative in response.json()["results"][0]["global_narratives"]:
    print(narrative["title"], narrative["sentiment"]["label"])
```

### Query multiple tickers at once
```python
response = requests.get(
    f"{BASE_URL}/v1/narratives/comprehensive",
    headers=headers,
    params={"tickers": "NVDA,AMD,TSLA", "from_date": "2026-05-01", "to_date": "2026-05-10"}
)
for result in response.json()["results"]:
    print(f"{result['ticker']}: {result['counts']['global_narrative_count']} narratives")
```

### Analyze portfolio narrative risk
```python
import json

holdings = [
    {"ticker": "NVDA", "weight": 0.30},
    {"ticker": "AAPL", "weight": 0.25},
    {"ticker": "TSLA", "weight": 0.20},
    {"ticker": "MSFT", "weight": 0.25},
]

response = requests.post(
    f"{BASE_URL}/v1/portfolio/narrative-risk",
    headers={**headers, "Content-Type": "application/json"},
    json={"holdings": holdings}
)

for theme in response.json()["themes"]:
    print(f"{theme['theme']}: {theme['tickers']} — {theme['sentiment']}")
```

### Use full history
```python
response = requests.get(
    f"{BASE_URL}/v1/narratives/comprehensive",
    headers=headers,
    params={"tickers": "NVDA", "all_time": "true"}
)
```

---

## Rate Limits

| Tier | Credits | History | Tickers |
|------|---------|---------|---------|
| Free Trial | 500 (one-time) | 90 days | 10 (TSLA, NVDA, AAPL, MSFT, AMZN, GOOGL, META, AMD, NFLX, JPM) |
| Plus | 2,500/month | 180 days | All 109 |
| Scale | Unlimited | Full history | All 109 |

Credits are consumed per ticker per day queried. When you exceed your credits, the API returns `HTTP 429`.

[→ Upgrade at aletaindex-narrative.com/subscription](https://aletaindex-narrative.com/subscription)

---

## Full API Reference

→ [api-reference.md](api-reference.md)
