<div align="center">

# 🧠 NEXUS — Enterprise Agentic Workflow AI System

**Production-grade multi-agent AI platform built with LangGraph, CrewAI, FastAPI, and LangSmith**

[![CI](https://github.com/ahamedafzal/enterprise-agentic-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/ahamedafzal/enterprise-agentic-ai/actions)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green.svg)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.1.19-orange.svg)](https://langchain-ai.github.io/langgraph)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Live Demo](#) · [API Docs](#) · [LangSmith Traces](#)

</div>

---

## 🎯 What is NEXUS?

NEXUS is a production-grade **Enterprise Agentic Workflow AI System** that mirrors how a senior analyst team works. Submit a complex business query — four specialised AI agents coordinate autonomously to retrieve documents, analyse data, search the web, and generate a structured executive report — all tracked in real time.

Built to align with **UAE National AI Strategy 2031** enterprise use cases.

---

## 🏗️ Architecture

```
User Query (React Dashboard)
         ↓
    FastAPI Backend
         ↓
  LangGraph Workflow Engine
         ↓
┌─────────────────────────────────┐
│     Orchestrator Agent          │  ← Decomposes query into subtasks
└──────────────┬──────────────────┘
               ↓
┌─────────────────────────────────┐
│     Document Analyst Agent      │  ← RAG over ChromaDB (re-ranked)
└──────────────┬──────────────────┘
               ↓
┌─────────────────────────────────┐
│     Data Retrieval Agent        │  ← Structured data + web search
└──────────────┬──────────────────┘
               ↓
┌─────────────────────────────────┐
│     Report Generator Agent      │  ← Executive report synthesis
└──────────────┬──────────────────┘
               ↓
   Structured Executive Report
         ↓
  LangSmith (full trace)
```

---

## 🤖 The 4 AI Agents

| Agent | Role | Tools |
|-------|------|-------|
| **Orchestrator** | Decomposes queries, routes subtasks | LangGraph, Groq LLM |
| **Document Analyst** | RAG over enterprise documents | ChromaDB, Cross-encoder re-ranking |
| **Data Retrieval** | Structured data + live web context | CSV/JSON parsing, DuckDuckGo |
| **Report Generator** | Executive report synthesis | Groq LLM, Markdown output |

---

## 🚀 Enterprise Use Cases

- **Project Risk Analysis** — *"Identify all delayed Q4 projects and suggest mitigation plans"*
- **Contract Intelligence** — *"Summarise key obligations in our vendor contracts"*
- **HR Insights** — *"Which departments have the highest attrition risk?"*
- **Executive Briefing** — *"Generate a board-ready AI initiative status report"*

---

## 🛠️ Tech Stack

### Agent Layer
- **LangGraph** — stateful workflow graph, sequential agent orchestration
- **LangChain** — LLM abstraction, prompt management
- **LangSmith** — full observability, traces, token usage, latency
- **Groq API** — ultra-fast LLM inference (llama-3.3-70b-versatile)

### RAG Pipeline
- **ChromaDB** — vector store with persistent embeddings
- **Sentence Transformers** — cross-encoder re-ranking (ms-marco-MiniLM-L-6-v2)
- **DuckDuckGo Search** — live web context for agents

### Backend
- **FastAPI** — async REST API, WebSocket, JWT auth
- **Celery + Redis** — async task queue
- **PostgreSQL** — workflow history, agent logs
- **SQLAlchemy** — async ORM

### Frontend
- **React 18** — dashboard UI
- **Tailwind CSS** — styling
- **React Router** — navigation
- **Axios** — API client

### Infrastructure
- **Docker Compose** — full stack containerisation
- **Nginx** — reverse proxy, static file serving
- **Prometheus** — metrics endpoint
- **GitHub Actions** — CI/CD pipeline

---

## ⚡ Quick Start

### Prerequisites
- Docker Desktop
- Python 3.11
- Node.js 20
- Groq API key (free at console.groq.com)
- LangSmith API key (free at smith.langchain.com)

### Run locally

```bash
# Clone
git clone https://github.com/ahamedafzal/enterprise-agentic-ai.git
cd enterprise-agentic-ai

# Setup environment
cp .env.example .env
# Add your GROQ_API_KEY and LANGCHAIN_API_KEY to .env

# Start infrastructure
docker-compose up -d postgres redis chromadb

# Install Python dependencies
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Generate synthetic datasets
python data/scripts/generate_data.py

# Ingest data into ChromaDB
python -m backend.core.ingest

# Start backend
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Start frontend (new terminal)
cd frontend && npm install && npm run dev
```

Open:
- Frontend: `http://localhost:5173`
- API Docs: `http://localhost:8000/docs`
- LangSmith: `https://smith.langchain.com`

### Run with Docker (production)

```bash
docker compose -f docker-compose.prod.yml up -d
```

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | JWT authentication |
| POST | `/workflow/run` | Run workflow async |
| GET | `/workflow/run-sync` | Run workflow sync |
| GET | `/workflow/status/{id}` | Check workflow status |
| GET | `/workflow/history` | All past workflows |
| GET | `/agents/` | List all agents |
| POST | `/documents/upload` | Upload document to RAG |
| GET | `/health/detailed` | Full system health |
| GET | `/metrics` | Prometheus metrics |
| WS | `/ws/workflow/{id}` | Real-time WebSocket |

---

## 🗄️ Synthetic Dataset

| Dataset | Records | Description |
|---------|---------|-------------|
| `employee_data.csv` | 500 | Employees with KPI, attrition risk, department |
| `project_reports.json` | 50 | Projects with status, budget, risks |
| `contracts.json` | 20 | Vendor contracts with obligations |
| `financial_summary.json` | 12 | Quarterly financials |

---

## 🔍 Observability

Every workflow run is fully traced in LangSmith:
- Per-agent token usage and latency
- Input/output for every LLM call
- Full workflow execution graph
- Error tracking and retry logs

Every HTTP request gets a unique `X-Trace-ID` header for end-to-end tracing.

---

## 📁 Project Structure

```
enterprise-agentic-ai/
├── backend/
│   ├── agents/
│   │   ├── orchestrator_agent.py
│   │   ├── document_analyst_agent.py
│   │   ├── data_retrieval_agent.py
│   │   ├── report_generator_agent.py
│   │   ├── workflow_graph.py
│   │   └── tools/
│   │       └── web_search.py
│   ├── api/routes/
│   │   ├── auth.py
│   │   ├── workflow.py
│   │   ├── agents.py
│   │   ├── documents.py
│   │   └── websocket.py
│   ├── core/
│   │   ├── config.py
│   │   ├── auth.py
│   │   ├── database.py
│   │   ├── logging.py
│   │   ├── middleware.py
│   │   └── reranker.py
│   └── services/
│       ├── workflow_service.py
│       └── health_service.py
├── frontend/
│   └── src/
│       ├── pages/
│       ├── components/
│       ├── store/
│       └── utils/
├── data/
│   ├── scripts/generate_data.py
│   └── synthetic/
├── infra/
│   ├── docker/
│   └── nginx/
└── .github/workflows/ci.yml
```

---

## 🌍 UAE AI Strategy Alignment

This project directly maps to **UAE National AI Strategy 2031** pillars:
- **Government AI** — automated report generation for decision makers
- **Enterprise AI** — multi-agent workflow automation
- **AI Talent** — demonstrates production-grade AI engineering skills

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

<div align="center">
Built for the UAE AI ecosystem
</div>