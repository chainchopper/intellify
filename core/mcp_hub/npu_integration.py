import os
import requests
import logging
from dotenv import load_dotenv

# Load env vars up to three levels up to find the central .env
current_dir = os.path.dirname(__file__)
env_path = os.path.abspath(os.path.join(current_dir, "..", "..", ".env"))
load_dotenv(dotenv_path=env_path)

NPU_API_URL = os.getenv("NPU_STACK_API_URL", "http://127.0.0.1:8000")

def trigger_npu_fine_tune(model_name: str, dataset_path: str, params: dict = None):
    """
    Triggers a fine-tuning job on the connected NPU-STACK instance.
    This simulates the bridge between the Intellify Management plane and NPU-STACK execution.
    """
    endpoint = f"{NPU_API_URL}/api/models/fine-tune"
    
    payload = {
        "base_model": "llama-2-7b", # Or inferred from params
        "dataset_path": dataset_path,
        "output_model_name": model_name,
        "epochs": params.get("epochs", 3) if params else 3,
        "batch_size": params.get("batch_size", 4) if params else 4,
        "learning_rate": params.get("learning_rate", 2e-5) if params else 2e-5
    }
    
    logging.info(f"[Intellify->NPU] Triggering fine-tune for {model_name} at {NPU_API_URL}")
    logging.info(f"Payload: {payload}")
    
    try:
        response = requests.post(endpoint, json=payload, timeout=20)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"[Intellify->NPU] Failed to trigger NPU-STACK: {e}")
        return {"error": str(e), "status": "FAILED"}

def fetch_npu_system_health():
    """
    Pulls hardware health metrics from NPU-STACK to display on Intellify Dashboard.
    """
    endpoint = f"{NPU_API_URL}/api/health"
    try:
        response = requests.get(endpoint, timeout=5)
        return response.json()
    except Exception as e:
        logging.error(f"[Intellify->NPU] Health check failed: {e}")
        return {"status": "UNREACHABLE", "npu_api": NPU_API_URL}
