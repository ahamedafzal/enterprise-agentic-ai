from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.services.workflow_service import get_workflow
import asyncio
import json

router = APIRouter(tags=["WebSocket"])

@router.websocket("/ws/workflow/{workflow_id}")
async def workflow_websocket(websocket: WebSocket, workflow_id: str):
    await websocket.accept()
    try:
        while True:
            workflow = get_workflow(workflow_id)
            if workflow:
                await websocket.send_text(json.dumps({
                    "workflow_id": workflow_id,
                    "status":      workflow["status"],
                    "has_result":  workflow.get("result") is not None,
                }))
                if workflow["status"] in ["completed", "failed"]:
                    break
            else:
                await websocket.send_text(json.dumps({
                    "workflow_id": workflow_id,
                    "status":      "not_found",
                }))
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass