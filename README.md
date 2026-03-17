# Narrative Intelligence API

**Give your AI agent a financial narrative brain.**

Narrative Intelligence tracks how financial stories evolve across thousands of news sources in real time — clustering articles into structured narratives, measuring sentiment momentum, and generating LLM-powered insights for TSLA, NVDA, AAPL, AMZN, GOOGL, META, MSFT, and AMD.

Instead of raw news feeds or simple sentiment scores, your agent gets **narrative-level intelligence**: what the market is talking about, how strongly, and whether it's shifting.

---

## What Your Agent Can Do

```
You: "What narratives are driving NVDA right now? Any sentiment shifts?"

Agent: NVDA is currently dominated by two narratives:
  1. "AI Infrastructure Supercycle" — 47 articles, sentiment +0.68, trending up
  2. "Export Control Headwinds" — 23 articles, sentiment -0.41, stable

  Anomaly detected: "Data Center Capex" spiked +340% mentions on Mar 14,
  correlating with MSFT earnings beat. Potential spillover signal.
```

No prompt engineering required. The agent knows how to query the data automatically.

---

## Supported Tickers

`TSLA` `NVDA` `AMD` `AAPL` `MSFT` `AMZN` `GOOGL` `META`

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

| Tier | Tickers | History | Calls/day | Price |
|------|---------|---------|-----------|-------|
| **Free** | TSLA only | 1 day | 100 | Free |
| **Pro** | All 8 | 90 days | 1,000 | $49/mo |
| **Enterprise** | All 8 + custom | Full history | Unlimited | Contact us |

**[→ Get your API key](https://aletaindex-narrative.com/register)**

---

## Quick Example

```python
import requests

headers = {"X-API-Key": "nk_your_key_here"}
params = {"tickers": "NVDA", "days": 7}

response = requests.get(
    "https://aletaindex-narrative.com/v1/narratives/comprehensive",
    headers=headers,
    params=params
)

data = response.json()
print(data["results"][0]["insights"]["summary"]["dominant_narrative"])
```

---

## Documentation

- [Dev Plan](docs/dev-plan.md) — roadmap and architecture decisions
- [API Reference](docs/api-reference.md) — all endpoints, parameters, response schemas
- [Data Model](docs/data-model.md) — narrative hierarchy explained
- [MCP Quickstart](mcp/README.md) — agent integration in 2 minutes
- [Direct API Guide](docs/direct-api-guide.md) — REST integration guide
- [Example Prompts](examples/strategy-prompts.md) — prompt templates for trading agents

---

## Contact

API access requests: **api@narrative-intelligence.com**
