from fastapi import APIRouter

router = APIRouter(prefix="/agents", tags=["Agents"])

AGENTS = [
    {
        "id":          "orchestrator",
        "name":        "Orchestrator Agent",
        "description": "Decomposes queries and routes to specialist agents",
        "tools":       ["LangGraph", "Groq LLM"],
        "status":      "active",
    },
    {
        "id":          "document_analyst",
        "name":        "Document Analyst Agent",
        "description": "RAG over enterprise documents using ChromaDB",
        "tools":       ["ChromaDB", "LangChain RAG", "Groq LLM"],
        "status":      "active",
    },
    {
        "id":          "data_retrieval",
        "name":        "Data Retrieval Agent",
        "description": "Queries structured data from CSVs and JSON files",
        "tools":       ["PostgreSQL", "Pandas", "Groq LLM"],
        "status":      "active",
    },
    {
        "id":          "report_generator",
        "name":        "Report Generator Agent",
        "description": "Synthesises findings into executive reports",
        "tools":       ["Groq LLM", "Pydantic"],
        "status":      "active",
    },
]

@router.get("/")
async def list_agents():
    return {"agents": AGENTS, "total": len(AGENTS)}

@router.get("/{agent_id}")
async def get_agent(agent_id: str):
    agent = next((a for a in AGENTS if a["id"] == agent_id), None)
    if not agent:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent