# AletaIndex Narrative Intelligence API

**Give your AI agent a financial narrative brain.**

AletaIndex tracks how financial stories evolve across thousands of news sources in real time — clustering articles into structured narratives, measuring sentiment momentum, and mapping narrative risk across portfolios. Available for 109 tickers across all major sectors.

Instead of raw news feeds or simple sentiment scores, your agent gets **narrative-level intelligence**: what the market is talking about, how strongly, and whether it's shifting.

---

## What Your Agent Can Do

```
You: "What narratives are driving NVDA right now? Any sentiment shifts?"

Agent: NVDA is currently dominated by two narratives:
  1. "AI Infrastructure Supercycle" — 47 articles, sentiment +0.68, trending up
  2. "Export Control Headwinds" — 23 articles, sentiment -0.41, stable

  Sentiment on "Export Control Headwinds" has improved +0.12 over the past week,
  suggesting the market is pricing in less risk from the latest policy signals.
```

No prompt engineering required. The agent knows how to query the data automatically.

---

## Two Ways to Integrate

### Option A — MCP Server (Recommended for AI Agents)
One-line config. Works with Claude Code, Cursor, Windsurf, and any MCP-compatible agent.
→ [MCP Quickstart](mcp/README.md)

### Option B — REST API
Direct HTTP calls. Works with any language or framework.
→ [API Reference](docs/api-reference.md)

---

## Pricing

| Tier | Tickers | History | Credits | Price |
|------|---------|---------|---------|-------|
| **Free Trial** | 10 tickers | 90 days | 500 (one-time) | Free, 7 days |
| **Plus** | All 109 tickers | 180 days | 2,500/month | $99/mo |
| **Scale** | All 109 tickers | Full history | Unlimited | Custom — [contact us](https://aletaindex-narrative.com) |

Free tickers: `TSLA` `NVDA` `AAPL` `MSFT` `AMZN` `GOOGL` `META` `AMD` `NFLX` `JPM`

**[→ Get your API key](https://aletaindex-narrative.com)**

---

## Quick Example

```python
import requests

headers = {"X-API-Key": "nk_your_key_here"}

response = requests.get(
    "https://aletaindex-narrative.com/v1/narratives/comprehensive",
    headers=headers,
    params={"tickers": "NVDA", "from_date": "2026-05-01", "to_date": "2026-05-10"},
)

data = response.json()
for narrative in data["results"][0]["global_narratives"]:
    print(narrative["title"], narrative["sentiment"]["avg_sentiment"])
```

---

## Documentation

- [API Reference](docs/api-reference.md) — endpoints, parameters, response schemas
- [Data Model](docs/data-model.md) — narrative hierarchy explained
- [MCP Quickstart](mcp/README.md) — agent integration in 2 minutes
- [Direct API Guide](docs/direct-api-guide.md) — REST integration guide
- [Example Prompts](examples/strategy-prompts.md) — prompt templates for trading agents
