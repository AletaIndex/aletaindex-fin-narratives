# Direct API Guide

Use the Narrative Intelligence REST API from any language or framework.

---

## Authentication

All requests require an API key in the header:

```
X-API-Key: nk_your_key_here
```

Get your key at [narrative-intelligence.com/register](https://aletaindex-narrative.com/register).

---

## Python

```python
import requests

API_KEY = "nk_your_key_here"
BASE_URL = "https://aletaindex-narrative.com"

headers = {"X-API-Key": API_KEY}

# Get narratives for NVDA — last 7 days
response = requests.get(
    f"{BASE_URL}/v1/narratives/comprehensive",
    headers=headers,
    params={"tickers": "NVDA", "days": 7}
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

async function getNarratives(ticker: string, days: number = 7) {
  const response = await fetch(
    `${BASE_URL}/v1/narratives/comprehensive?tickers=${ticker}&days=${days}`,
    { headers: { "X-API-Key": API_KEY } }
  );
  return response.json();
}

const data = await getNarratives("NVDA", 7);
console.log(data.results[0].insights.summary.dominant_narrative);
```

---

## Common Patterns

### Get dominant narrative + sentiment trend
```python
response = requests.get(
    f"{BASE_URL}/v1/narratives/insights",
    headers=headers,
    params={"ticker": "TSLA", "days": 30}
)
insights = response.json()["insights"]
print(insights["summary"]["dominant_narrative"]["title"])
print(insights["summary"]["overall_sentiment_trend"])
```

### Get narrative timeline for charting
```python
response = requests.get(
    f"{BASE_URL}/v1/narratives/timeline",
    headers=headers,
    params={"ticker": "AAPL", "days": 90}
)
timeline = response.json()
# Returns per-date: sentiment, article_count, top 5 narratives
```

### Check for anomalies
```python
response = requests.get(
    f"{BASE_URL}/v1/narratives/insights",
    headers=headers,
    params={"ticker": "NVDA", "days": 7}
)
anomalies = response.json()["insights"]["anomalies"]
for a in anomalies:
    if a["severity"] == "high":
        print(f"[{a['date']}] {a['type']}: {a['description']}")
```

### Query multiple tickers
```python
response = requests.get(
    f"{BASE_URL}/v1/narratives/comprehensive",
    headers=headers,
    params={"tickers": "NVDA,AMD,TSLA", "days": 7}
)
for result in response.json()["results"]:
    print(f"{result['ticker']}: {result['counts']['global_narrative_count']} narratives")
```

---

## Rate Limits

| Tier | Limit |
|------|-------|
| Free | 100 calls/day, TSLA only, 1-day history |
| Pro | 1,000 calls/day, all tickers, 90-day history |
| Enterprise | Unlimited |

When you exceed the limit, the API returns `HTTP 429` with a message indicating when the limit resets.

---

## Full API Reference

→ [api-reference.md](api-reference.md)
