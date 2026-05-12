import os
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
import structlog

from backend.agents.orchestrator_agent import OrchestratorAgent
from backend.agents.document_analyst_agent import DocumentAnalystAgent
from backend.agents.data_retrieval_agent import DataRetrievalAgent
from backend.agents.report_generator_agent import ReportGeneratorAgent

# Set LangSmith env vars programmatically as backup
os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")

logger = structlog.get_logger()

# ── Shared workflow state ────────────────────────────────────────────────────
class WorkflowState(TypedDict):
    query:             str
    subtasks:          Optional[list]
    document_findings: Optional[str]
    data_findings:     Optional[str]
    final_report:      Optional[str]
    status:            str
    error:             Optional[str]

# ── Node functions ───────────────────────────────────────────────────────────
async def orchestrate_node(state: WorkflowState) -> WorkflowState:
    logger.info("Node: orchestrate", query=state["query"])
    agent  = OrchestratorAgent()
    result = await agent.run({"query": state["query"]})
    return {**state, "subtasks": result["output"]["subtasks"], "status": "orchestrated"}

async def document_analysis_node(state: WorkflowState) -> WorkflowState:
    logger.info("Node: document_analysis")
    agent  = DocumentAnalystAgent()
    task   = next(
        (t["task"] for t in (state["subtasks"] or []) if t["agent"] == "document_analyst"),
        "Analyse all relevant documents for this query",
    )
    result = await agent.run({"task": task, "query": state["query"]})
    return {**state, "document_findings": result["output"], "status": "documents_analysed"}

async def data_retrieval_node(state: WorkflowState) -> WorkflowState:
    logger.info("Node: data_retrieval")
    agent  = DataRetrievalAgent()
    task   = next(
        (t["task"] for t in (state["subtasks"] or []) if t["agent"] == "data_retrieval"),
        "Retrieve and analyse all relevant structured data",
    )
    result = await agent.run({"task": task, "query": state["query"]})
    return {**state, "data_findings": result["output"], "status": "data_retrieved"}

async def report_generation_node(state: WorkflowState) -> WorkflowState:
    logger.info("Node: report_generation")
    agent  = ReportGeneratorAgent()
    result = await agent.run({
        "query":             state["query"],
        "document_findings": state.get("document_findings", ""),
        "data_findings":     state.get("data_findings", ""),
    })
    return {**state, "final_report": result["output"], "status": "completed"}

# ── Build the graph ──────────────────────────────────────────────────────────
def build_graph():
    workflow = StateGraph(WorkflowState)

    workflow.add_node("orchestrate",       orchestrate_node)
    workflow.add_node("document_analysis", document_analysis_node)
    workflow.add_node("data_retrieval",    data_retrieval_node)
    workflow.add_node("report_generation", report_generation_node)

    workflow.set_entry_point("orchestrate")
    workflow.add_edge("orchestrate",       "document_analysis")
    workflow.add_edge("document_analysis", "data_retrieval")
    workflow.add_edge("data_retrieval",    "report_generation")
    workflow.add_edge("report_generation", END)

    return workflow.compile()

graph = build_graph()