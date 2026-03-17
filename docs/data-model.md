# Data Model

## Narrative Hierarchy

Narrative Intelligence organizes financial news into a three-level hierarchy:

```
Global Narrative
└── Daily Topic (per day)
    └── Article
```

### Level 1: Global Narrative
A persistent story that spans days or weeks. Created when a cluster of related articles first appears, and updated daily as new articles are matched.

Examples:
- *"AI Infrastructure Supercycle"*
- *"Export Control Headwinds"*
- *"Autonomous Vehicle Regulatory Progress"*

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Unique narrative ID |
| `title` | string | LLM-generated descriptive title |
| `created_at` | datetime | When this narrative first appeared |
| `last_updated_at` | datetime | Last time new articles were added |
| `metadata.article_count` | int | Total articles in this narrative |
| `metadata.daily_topic_count` | int | Number of days with activity |
| `sentiment.avg_sentiment` | float (-1–1) | Dominance-weighted average sentiment |
| `sentiment.label` | string | `positive` / `negative` / `neutral` |

---

### Level 2: Daily Topic
A snapshot of how a narrative manifested on a specific day. Each day produces a new daily topic if enough articles cluster together.

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Unique daily topic ID |
| `title` | string | Day-specific title (may differ from parent narrative) |
| `time` | date | The date this topic covers |
| `dominance_score` | float (0–1) | How dominant this topic was that day |
| `article_count` | int | Articles published this day |
| `avg_sentiment` | float (-1–1) | Average sentiment across articles |

**Dominance Score Formula:**
```
dominance = mention_score × 50%
           + sentiment_magnitude × 30%
           + recency_weight × 20%
```

---

### Level 3: Article
Individual news articles, enriched with relevance and sentiment scores.

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Article ID |
| `title` | string | Headline |
| `source` | string | Publisher name |
| `link` | string | Original URL |
| `published_at` | datetime | Publication time (UTC) |
| `representativeness_score` | float (0–1) | How central this article is to the topic |
| `ticker_relevance_score` | float (0–1) | How relevant this article is to the queried ticker |
| `rank_in_topic` | int | 1 = most relevant article in topic |
| `sentiment.score` | float (-1–1) | Sentiment score |
| `sentiment.label` | string | `positive` / `negative` / `neutral` |
| `is_duplicate` | bool | Near-duplicate of another article |

---

## Insights Object

LLM-generated analysis returned by `/v1/narratives/insights` and embedded in the comprehensive response.

```json
{
  "summary": {
    "dominant_narrative": {
      "title": "AI Infrastructure Supercycle",
      "trend": "accelerating",
      "sentiment": 0.68
    },
    "overall_sentiment_score": 0.42,
    "overall_sentiment_label": "positive",
    "overall_sentiment_trend": "improving",
    "sentiment_trend_magnitude": 0.15
  },
  "key_insights": [
    {
      "insight": "Data center capex narrative surged 340% in mentions on Mar 14",
      "category": "spike",
      "priority": "high",
      "supporting_data": {
        "narrative_title": "Data Center Capex",
        "metric": "mention_count",
        "value": 34,
        "change": "+340%",
        "time_range": "1 day",
        "date": "2026-03-14"
      }
    }
  ],
  "anomalies": [
    {
      "date": "2026-03-14",
      "type": "mention_spike",
      "description": "Unusual surge in data center articles following MSFT earnings",
      "severity": "high",
      "narrative_title": "Data Center Capex"
    }
  ],
  "correlations": [
    {
      "type": "narrative_narrative",
      "description": "AI Infrastructure and Data Center Capex narratives co-move with +0.82 correlation",
      "correlation": 0.82,
      "direction": "positive",
      "lag_days": 1,
      "narrative_title": "AI Infrastructure Supercycle"
    }
  ]
}
```

---

## Sentiment Scale

| Range | Label |
|-------|-------|
| +0.3 to +1.0 | positive |
| -0.3 to +0.3 | neutral |
| -1.0 to -0.3 | negative |

Sentiment is computed at the article level and aggregated up using dominance-weighted averaging at the daily topic and global narrative levels.
