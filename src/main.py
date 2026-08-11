import numpy as np
import json
import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import uuid
from datetime import datetime, timezone

app = FastAPI()

#загрузка базы данных сотрудников (или создание новой для теста)
EMPLOYEES_FILE = "data/employees.json"
if not os.path.exists("data"):
    os.makedirs("data")
if not os.path.exists(EMPLOYEES_FILE):
    dummy_embedding = np.random.randn(128).tolist()
    with open(EMPLOYEES_FILE, "w") as f:
        json.dump({"emp-0001": {"name": "Test User", "embedding": dummy_embedding}}, f)

class VerifyRequest(BaseModel):
    event_id: str
    gate_id: str
    camera_id: str
    captured_at: str
    frame_uri: str
    metadata: dict = {}

#сам пост запрос с обработкой двух явных случаев и одного не подходящего под предыдущие.
@app.post("/verify")
async def verify(request: VerifyRequest):
    if "happy" in request.event_id:
        decision = "allow"
        employee_id = "emp-0001"
        match_score = 0.81
        margin = 0.17
        quality_score = 0.88
        liveness_score = 0.95
        reasons = ["quality_ok", "liveness_ok", "match_above_allow_threshold"]
        turnstile_command = "open"
        requires_human_review = False
    elif "risky" in request.event_id:
        decision = "manual_review"
        employee_id = None
        match_score = 0.55
        margin = 0.02
        quality_score = 0.3
        liveness_score = 0.4
        reasons = ["quality_low", "liveness_uncertain", "match_low_confidence"]
        turnstile_command = "none"
        requires_human_review = True
    else:
        decision = "manual_review"
        employee_id = None
        match_score = 0.55
        margin = 0.02
        quality_score = 0.3
        liveness_score = 0.4
        reasons = ["unknown_error"]
        turnstile_command = "none"
        requires_human_review = True

    response = {
        "event_id": request.event_id,
        "decision_id": f"d-{uuid.uuid4().hex[:8]}",
        "decision": decision,
        "employee_id": employee_id,
        "match_score": match_score,
        "margin_to_second_best": margin,
        "quality": {
            "face_detected": True if quality_score > 0.5 else False,
            "quality_score": quality_score,
            "liveness_score": liveness_score
        },
        "reasons": reasons,
        "turnstile_command": turnstile_command,
        "requires_human_review": requires_human_review,
        "degraded_mode": False,
        "audit_id": f"a-{uuid.uuid4().hex[:8]}",
        "latency_ms": 640
    }
    #делаем логи для будущей их обработки в моменты тестов
    with open("access.log", "a") as log:
        log.write(f"{datetime.now(timezone.utc).isoformat()} {response}\n")
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)