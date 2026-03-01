import os
import json
import uuid
import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from npu_integration import trigger_npu_fine_tune, fetch_npu_system_health
import db

app = FastAPI(title="Intellify MCP Hub", description="Hybrid Orchestrator for Intellify Local & Cloud Tasks")
logging.basicConfig(level=logging.INFO)

class RecommendationRequest(BaseModel):
    category: str
    file_format: str
    asset_count: int

class TaskControl(BaseModel):
    task_id: str
    action: str  # "start", "pause", "cancel"

@app.post("/api/recommendations")
def get_recommendations(req: RecommendationRequest):
    """
    Service Recommendation Engine:
    Evaluates incoming metadata and recommends appropriate Intellify Docker pipelines.
    """
    recommended_services = []
    
    # PDF Ingestion Logic
    if req.category == "financial_reports" and req.file_format == ".pdf" and req.asset_count >= 10:
        recommended_services.append({
            "service_id": "pdf-ingestion",
            "name": "PDF Ingestion Service",
            "container": "intellify-ingestion-service:pdf-v1.2",
            "description": "Extracts text via pdfminer.six and prepares for training"
        })
    
    # Document Analytics Logic
    if req.category == "internal_memo" and req.file_format in [".doc", ".docx"] and req.asset_count >= 50:
         recommended_services.append({
            "service_id": "hr-analytics",
            "name": "HR Analytics Agent",
            "container": "intellify-training-pipeline:hr-analytics-v1.0",
            "description": "Analyzes internal memos to generate organizational insights"
        })

    # Default fallback
    if not recommended_services:
        recommended_services.append({
            "service_id": "generic-classifier",
            "name": "General File Classifier",
            "container": "intellify-ingestion-service:generic-v1.0",
            "description": f"Handles {req.file_format} files for general ingestion."
        })

    return {"recommendations": recommended_services}

@app.post("/api/tasks/opt-in")
def opt_in_task(service_id: str):
    """Admin triggers a recommended service to start from the UI."""
    task_id = f"task_{uuid.uuid4().hex[:8]}"
    db.create_task(
        task_id=task_id,
        service_id=service_id,
        status="STARTING",
        progress="0%",
        started_at=datetime.datetime.now().isoformat()
    )
    
    npu_relay_status = None
    # Check if this pipeline requires NPU-STACK fine-tuning
    if service_id == "hr-analytics":
        # Forwarding the ingested data over to NPU-STACK for training
        npu_response = trigger_npu_fine_tune(
            model_name="intellify-hr-analyzer-v1",
            dataset_path="/data/internal_memos/"  # Path representing the output of ingestion
        )
        db.update_task_npu_status(task_id, npu_response)
        npu_relay_status = npu_response
        logging.info(f"Triggered NPU-STACK fine-tuning job for {service_id}: {npu_response}")
        
    logging.info(f"Task {task_id} opted in for service {service_id}")
    return {"task_id": task_id, "status": "STARTING", "npu_relay": npu_relay_status}

@app.post("/api/tasks/control")
def control_task(req: TaskControl):
    """User opts out, pauses, or cancels an active task."""
    task = db.get_task(req.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    action = req.action.upper()
    valid_actions = ["PAUSE", "CANCEL", "RESUME", "REVERT"]
    
    if action not in valid_actions:
         raise HTTPException(status_code=400, detail=f"Invalid action. Allowed: {valid_actions}")
         
    if action == "RESUME":
        db.update_task_status(req.task_id, "INGESTING")
    else:
        db.update_task_status(req.task_id, action + "D")

    return {"task_id": req.task_id, "state": db.get_task(req.task_id)}

@app.get("/api/tasks")
def list_tasks():
    """Returns the state of all active tasks for the Dashboard to monitor."""
    return {"tasks": db.get_all_tasks()}

@app.get("/api/npu/status")
def npu_health_check():
    """Pings the NPU-STACK backend to verify the connection is alive."""
    return fetch_npu_system_health()

if __name__ == "__main__":
    db.init_db()
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)
