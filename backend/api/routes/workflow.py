import uuid
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
from backend.core.auth import get_current_user
from backend.services.workflow_service import (
    run_workflow_async,
    get_workflow,
    list_workflows,
)

router = APIRouter(prefix="/workflow", tags=["Workflow"])

class WorkflowRequest(BaseModel):
    query: str

class WorkflowResponse(BaseModel):
    id:         str
    query:      str
    status:     str
    created_at: str
    result:     Optional[dict] = None
    error:      Optional[str]  = None

@router.post("/run", response_model=WorkflowResponse)
async def run_workflow(
    request:          WorkflowRequest,
    background_tasks: BackgroundTasks,
    current_user:     dict = Depends(get_current_user),
):
    workflow_id = str(uuid.uuid4())
    background_tasks.add_task(run_workflow_async, workflow_id, request.query)
    return WorkflowResponse(
        id=workflow_id,
        query=request.query,
        status="queued",
        created_at="now",
    )

@router.get("/run-sync", response_model=WorkflowResponse)
async def run_workflow_sync(
    query:        str,
    current_user: dict = Depends(get_current_user),
):
    """Run workflow synchronously — useful for testing."""
    workflow_id = str(uuid.uuid4())
    result = await run_workflow_async(workflow_id, query)
    return WorkflowResponse(**result)

@router.get("/status/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow_status(
    workflow_id:  str,
    current_user: dict = Depends(get_current_user),
):
    workflow = get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return WorkflowResponse(**workflow)

@router.get("/history", response_model=list[WorkflowResponse])
async def get_workflow_history(
    current_user: dict = Depends(get_current_user),
):
    return [WorkflowResponse(**w) for w in list_workflows()]