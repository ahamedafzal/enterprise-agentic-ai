# NEXUS — Architecture & Design Decisions

## System Overview

NEXUS follows a **sequential multi-agent architecture** where each agent
builds on the previous agent's findings — mirroring how a real analyst team works.

## Why Sequential, Not Parallel?

The agents run sequentially by design:

```
Orchestrator → Document Analyst → Data Retrieval → Report Generator
```

**Document Analyst runs first** because it reads unstructured documents
(contracts, reports) and its findings provide context for the Data Retrieval
Agent to fetch more targeted structured data.

Running them in parallel would mean the Data Retrieval Agent starts blind
without document context — producing lower quality reports.

## RAG Pipeline Design

```
User Query
    ↓
ChromaDB vector search (n=8, cosine similarity)
    ↓
Cross-encoder re-ranking (ms-marco-MiniLM-L-6-v2)
    ↓
Top 3 most relevant documents
    ↓
LLM context window
```

**Why re-ranking?**
Vector similarity is fast but approximate — it compares query and document
as separate vectors. A cross-encoder reads query + document together,
producing more accurate relevance scores. We fetch 8 candidates and re-rank
to top 3, reducing noise in the LLM context.

## Agent Retry Strategy

All agents use exponential backoff via `tenacity`:
- Max attempts: 3
- Wait: 2s → 4s → 8s
- Handles Groq API rate limits gracefully

## Observability Stack

```
Every request → X-Trace-ID header (8-char UUID)
Every agent call → LangSmith trace
Every HTTP endpoint → Prometheus metrics
Every log line → structlog JSON with trace_id
```

## Data Flow

```
Synthetic Data (Faker)
    ↓
ChromaDB ingestion (text → embeddings → stored)
    ↓
Agent retrieval (query → embedding → cosine search → re-rank)
    ↓
LLM synthesis (context + prompt → structured report)
    ↓
React UI (markdown rendered report)
```

## Technology Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| LLM | Groq (llama-3.3-70b) | Free tier, fastest inference |
| Vector DB | ChromaDB | Easiest setup, built-in embeddings |
| Re-ranker | ms-marco-MiniLM-L-6-v2 | Best speed/quality tradeoff |
| Workflow | LangGraph | Production standard for agentic systems |
| Observability | LangSmith | Native LangGraph integration |
| Auth | JWT + bcrypt | Stateless, production standard |
| Task Queue | Celery + Redis | Production async pattern |