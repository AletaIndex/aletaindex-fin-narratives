# MCP Quickstart

Connect AletaIndex to any MCP-compatible AI agent in under 2 minutes.

**Compatible with:** Claude Code, Cursor, Windsurf, and any MCP-supporting tool.

---

## Step 1 — Get an API Key

[Sign up at aletaindex-narrative.com](https://aletaindex-narrative.com)

Free trial: 10 tickers, 90 days history, 500 credits.

---

## Prerequisites — Install `uv`

The MCP server runs via `uvx`, which is part of [`uv`](https://docs.astral.sh/uv/) — a fast Python package manager. If you don't have it yet:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then restart your terminal. `uvx` will be available automatically. No other setup needed.

---

## Step 2 — Add to Your Agent Config

### Claude Code

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "aletaindex": {
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

### Cursor / Windsurf

Add to your MCP config file:

```json
{
  "mcpServers": {
    "aletaindex": {
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
Has TSLA sentiment shifted in the last 3 days?
```

```
Analyze narrative risk across my portfolio: NVDA 30%, AAPL 25%, TSLA 20%, MSFT 25%
```

The agent automatically calls the right tools and formats the response.

---

## Available Tools

| Tool | Description |
|------|-------------|
| `get_narratives` | Full narrative hierarchy for one or more tickers: global narratives, daily topic clusters, articles, and sentiment scores |
| `get_portfolio_risk` | Macro risk theme analysis across a portfolio — identifies which narratives create concentrated exposure across multiple holdings |

---

## Example Agent Session

```
You: What's the narrative situation for NVDA right now?

Agent: [calls get_narratives(tickers="NVDA", from_date="2026-05-03", to_date="2026-05-10")]

NVDA — Last 7 Days

Active Narratives (5):
1. AI Infrastructure Supercycle — +0.68 sentiment, 47 articles, ESCALATING
2. Export Control Headwinds — -0.41 sentiment, 23 articles, stable
3. Data Center Capex Cycle — +0.55 sentiment, 18 articles, new spike May 7
4. Blackwell GPU Supply Chain — +0.31 sentiment, 12 articles, stable
5. China Market Access — -0.22 sentiment, 8 articles, declining

Sentiment on "Export Control Headwinds" improved +0.12 over the week,
suggesting the market is discounting near-term regulatory risk.
```

---

## Manual Installation (alternative to uvx)

```bash
pip install narrative-intelligence-mcp
```

Then use `narrative-intelligence-mcp` as the command instead of `uvx narrative-intelligence-mcp`.

---

## Troubleshooting

**"NARRATIVE_API_KEY is not set"** — Add your API key to the `env` section of your MCP config.

**"Rate limit exceeded"** — You've used all your credits. [Upgrade at aletaindex-narrative.com/subscription](https://aletaindex-narrative.com/subscription).

**"Access denied: Ticker X requires Plus tier"** — This ticker is not included in the free tier. [Upgrade at aletaindex-narrative.com/subscription](https://aletaindex-narrative.com/subscription). Free tickers: TSLA, NVDA, AAPL, MSFT, AMZN, GOOGL, META, AMD, NFLX, JPM.

---

## Prefer REST API?

→ [API Reference](../docs/api-reference.md)
