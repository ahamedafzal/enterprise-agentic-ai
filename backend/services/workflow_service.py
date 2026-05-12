import asyncio
import uuid
from datetime import datetime
from typing import Optional
import structlog

from backend.agents.workflow_graph import graph

logger = structlog.get_logger()

# In-memory store for workflow status (replaced by DB in production)
workflow_store: dict = {}

async def run_workflow_async(workflow_id: str, query: str) -> dict:
    """Run the full agentic workflow and store results."""
    logger.info("Starting workflow", workflow_id=workflow_id, query=query)

    workflow_store[workflow_id] = {
        "id":         workflow_id,
        "query":      query,
        "status":     "running",
        "created_at": datetime.utcnow().isoformat(),
        "result":     None,
        "error":      None,
    }

    try:
        initial_state = {
            "query":             query,
            "subtasks":          None,
            "document_findings": None,
            "data_findings":     None,
            "final_report":      None,
            "status":            "pending",
            "error":             None,
        }

        result = await graph.ainvoke(initial_state)

        workflow_store[workflow_id].update({
            "status":       "completed",
            "completed_at": datetime.utcnow().isoformat(),
            "result": {
                "final_report":      result.get("final_report"),
                "document_findings": result.get("document_findings"),
                "data_findings":     result.get("data_findings"),
                "subtasks":          result.get("subtasks"),
            },
        })

        logger.info("Workflow completed", workflow_id=workflow_id)
        return workflow_store[workflow_id]

    except Exception as e:
        logger.error("Workflow failed", workflow_id=workflow_id, error=str(e))
        workflow_store[workflow_id].update({
            "status": "failed",
            "error":  str(e),
        })
        return workflow_store[workflow_id]

def get_workflow(workflow_id: str) -> Optional[dict]:
    return workflow_store.get(workflow_id)

def list_workflows() -> list:
    return list(workflow_store.values())