# MCP Quickstart

Connect Narrative Intelligence to any MCP-compatible AI agent in under 2 minutes.

**Compatible with:** Claude Code, Cursor, Windsurf, and any MCP-supporting tool.

---

## Step 1 — Get an API Key

[Register for free at aletaindex-narrative.com](https://aletaindex-narrative.com/register)

Free tier includes: TSLA, last 1 day, 100 calls/day.

---

## Step 2 — Add to Your Agent Config

### Claude Code

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "narrative-intelligence": {
      "command": "uvx",
      "args": ["narrative-intelligence-mcp"],
      "env": {
        "NARRATIVE_API_KEY": "nk_your_key_here"
      }
    }
  }
}
```

Restart Claude Code. Done.

### Cursor

Add to your Cursor MCP config:

```json
{
  "mcpServers": {
    "narrative-intelligence": {
      "command": "uvx",
      "args": ["narrative-intelligence-mcp"],
      "env": {
        "NARRATIVE_API_KEY": "nk_your_key_here"
      }
    }
  }
}
```

---

## Step 3 — Start Asking

No setup prompts needed. Just ask naturally:

```
What narratives are driving NVDA this week?
```

```
Has TSLA's sentiment shifted in the last 3 days?
```

```
Show me the dominant narrative for AAPL and compare it to last month.
```

```
Are there any anomalies in AMD's narrative coverage today?
```

The agent automatically calls the right tools and formats the response.

---

## Available Tools

Once connected, your agent has access to:

| Tool | Description |
|------|-------------|
| `get_narratives` | Full narrative hierarchy: global narratives → daily topics → articles |
| `get_insights` | LLM-generated analysis: summary, anomalies, correlations, trends |
| `get_timeline` | Sentiment and mention volume over time |
| `get_price` | OHLCV price data with daily returns |

---

## Example Agent Session

```
You: What's the market narrative situation for NVDA right now?

Agent: [calls get_narratives(ticker="NVDA", days=7)]
       [calls get_insights(ticker="NVDA", days=7)]

NVDA — Last 7 Days Narrative Summary

Active Narratives (5):
1. AI Infrastructure Supercycle — +0.68 sentiment, 47 articles, ACCELERATING
2. Export Control Headwinds — -0.41 sentiment, 23 articles, stable
3. Data Center Capex Cycle — +0.55 sentiment, 18 articles, new spike Mar 14
4. Blackwell GPU Supply Chain — +0.31 sentiment, 12 articles, stable
5. China Market Access — -0.22 sentiment, 8 articles, declining

Key Insight: Data Center Capex surged +340% in mentions on Mar 14,
likely spillover from MSFT earnings. Positive sentiment divergence
from Export Control narrative suggests market is discounting
regulatory risk.

Anomaly: Sentiment flipped from -0.3 to +0.6 on Mar 12 within
the Export Control narrative — possible regulatory news catalyst.
```

---

## Manual Installation (alternative to uvx)

```bash
pip install narrative-intelligence-mcp
```

Then use `narrative-intelligence-mcp` as the command instead of `uvx narrative-intelligence-mcp`.

---

## Troubleshooting

**"No tools available"** — Check that your API key is set correctly in the env config.

**"Free tier limit exceeded"** — You've hit 100 calls/day. [Upgrade to Pro](https://aletaindex-narrative.com/register).

**"Ticker not available on free tier"** — Free tier is TSLA only. [Upgrade to Pro](https://aletaindex-narrative.com/register) for all 8 tickers.

---

## Prefer REST API?

→ [Direct API Guide](../docs/direct-api-guide.md)
