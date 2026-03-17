# Dev Plan — Narrative Intelligence Public API

## Goal

Monetize the Narrative Intelligence pipeline by exposing it as a developer-friendly API and MCP server, targeting AI agent builders and quantitative developers.

---

## Phase 1 — Public Launch (2 weeks)

### 1.1 GitHub Repo (this repo)
- [x] README with product intro and pricing
- [x] API reference documentation
- [x] Data model documentation
- [x] MCP quickstart guide
- [x] Example prompts for trading agents
- [ ] Add demo screenshots / GIF of agent using the API

### 1.2 API Tier Enforcement
- [ ] Add free tier logic to auth middleware:
  - Restrict to `TSLA` only
  - Restrict to last 1 day of data
  - Cap at 100 calls/day
- [ ] Add tier field to `api_customers` table (`free` | `pro` | `enterprise`)
- [ ] Return clear error when free tier limit exceeded

### 1.3 Self-Serve Registration
- [ ] Existing `/register` page already works — verify email flow end-to-end
- [ ] Add tier selection on registration (free auto-approved, pro → payment)
- [ ] Add Stripe payment link for Pro tier ($49/mo)

### 1.4 MCP Server (separate repo: `narrative-intelligence-mcp`)
- [ ] Build Python MCP server with 3 core tools:
  - `get_narratives` — comprehensive narrative data
  - `get_insights` — LLM-generated narrative insights
  - `get_price` — OHLCV + daily return
- [ ] Publish to PyPI as `narrative-intelligence-mcp`
- [ ] Test end-to-end with Claude Code

---

## Phase 2 — Growth (Month 2)

### 2.1 Expand Ticker Coverage
- Add more tickers based on user requests
- Consider SPY, QQQ, BTC for macro narrative tracking

### 2.2 Webhook / Streaming
- Push notifications when narrative dominance shifts above threshold
- Target: algo trading systems that need real-time triggers

### 2.3 Agent Templates
- Pre-built agent configs for common use cases:
  - Daily market briefing agent
  - Narrative momentum trading signal
  - Earnings narrative tracker

---

## Phase 3 — Enterprise (Month 3+)

### 3.1 Custom Tickers
- Allow enterprise customers to request coverage of specific tickers

### 3.2 Source Credibility Layer
- Expose credibility scores per news source (from credibility engine)
- Premium add-on: weight narratives by source credibility

### 3.3 API v2
- (source, ticker) granularity for credibility
- Multi-window price validation (3/7/15/30d)
- Narrative prediction endpoint

---

## Architecture Overview

```
User / AI Agent
      │
      ▼
MCP Server (narrative-intelligence-mcp)   ← thin wrapper
      │
      ▼
REST API (narrative-intelligence, GCP)    ← your existing production API
      │
      ▼
PostgreSQL + Pipeline                     ← private, never exposed
```

### Key Design Decisions

**Why MCP first?**
MCP is the fastest path to agent adoption. One config line gives any Claude Code / Cursor user access to all narrative tools — no custom integration needed. REST API is available for non-agent use cases.

**Why keep the repo documentation-only?**
The pipeline, DB schema, and clustering algorithms are the moat. The public repo is a sales tool, not an open-source project.

**Why free tier on TSLA only?**
TSLA has the highest retail interest and most narrative activity, making it the best demo ticker. Limits prevent abuse while still giving real value.

---

## Immediate Next Steps (This Week)

1. Add free tier logic to `app/api/middleware/auth.py`
2. Create `narrative-intelligence-mcp` Python package
3. Test MCP server with Claude Code locally
4. Record a demo GIF showing the agent in action
5. Push this repo to GitHub (public)
