import os
import json
from datetime import datetime
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

app = FastMCP("NiaFlow-MCP")
LOCAL_DB_PATH = "niaflow_queue_state.json"

if not os.path.exists(LOCAL_DB_PATH):
    with open(LOCAL_DB_PATH, "w") as f:
        json.dump({"queue": [], "logs": []}, f)

class TriageVitals(BaseModel):
    sbp: int = Field(..., description="Systolic Blood Pressure (mmHg)")
    pulse: int = Field(..., description="Heart Rate / Pulse (bpm)")
    temp: float = Field(..., description="Temperature in Celsius")
    rr: int = Field(..., description="Respiratory Rate (breaths/min)")
    mobility: str = Field(..., description="Mobility status: 'walking', 'with_help', or 'immobile'")
    trauma: bool = Field(..., description="Is trauma present? True/False")

class ApprovalPayload(BaseModel):
    patient_id: str
    proposed_priority: str
    rationale: str
    clinician_name: str

@app.tool()
def calculate_tews_score(vitals: Dict[str, Any]) -> Dict[str, Any]:
    """Computes deterministic SATS Triage Early Warning Score (TEWS)."""
    score = 0
    v = TriageVitals(**vitals)
    
    if v.pulse < 40 or v.pulse > 130: score += 3
    elif (41 <= v.pulse <= 50) or (111 <= v.pulse <= 130): score += 2
    elif (51 <= v.pulse <= 60) or (101 <= v.pulse <= 110): score += 1
    
    if v.sbp < 70 or v.sbp > 220: score += 3
    elif (71 <= v.sbp <= 80) or (200 <= v.sbp <= 220): score += 2
    elif (81 <= v.sbp <= 100) or (171 <= v.sbp <= 199): score += 1
    
    if v.rr < 9 or v.rr > 30: score += 3
    elif (22 <= v.rr <= 30): score += 2
    elif (9 <= v.rr <= 14) or (15 <= v.rr <= 21): score += 1
    
    if v.temp < 35.0 or v.temp > 38.5: score += 2
    elif (35.0 <= v.temp <= 35.9) or (37.5 <= v.temp <= 38.4): score += 1

    if v.mobility == "immobile": score += 2
    elif v.mobility == "with_help": score += 1
    if v.trauma: score += 1

    color = "Green"
    if score >= 7: color = "Red"
    elif score >= 5: color = "Orange"
    elif score >= 3: color = "Yellow"

    return {"tews_score": score, "calculated_priority": color, "framework": "SATS_Standard"}

@app.tool()
def emergency_clinical_override(patient_id: str, trigger_complaint: str) -> Dict[str, Any]:
    """CRITICAL OVERRIDE: Uses ABC indicators to handle multi-patient surges in the Emergency Unit."""
    abc_compromised = ["airway", "choking", "stridor", "breathing", "cyanosis", "apnea", "circulation", "shock", "hemorrhage", "bleeding", "trampled", "somersaulted", "fracture"]
    match = any(indicator in trigger_complaint.lower() for indicator in abc_compromised)
    
    if match:
        return {
            "action": "IMMEDIATE_RED_BYPASS",
            "patient_id": patient_id,
            "priority": "RED",
            "routing": "Emergency Unit Resuscitation Bay (UCTH ER Floor Protocol)",
            "instruction": "Airway/Breathing/Circulation compromise detected. Bypass standard lines instantly."
        }
    return {"action": "STANDARD_FLOW", "message": "Patient stable. Route to standard evaluation queue."}

@app.tool()
def stage_human_approval(payload: Dict[str, Any]) -> str:
    """Irreversible Action Gate: Validates and logs clinical decisions locally to prevent file loss."""
    data = ApprovalPayload(**payload)
    timestamp = datetime.utcnow().isoformat()
    
    entry = {
        "timestamp": timestamp,
        "patient_id": data.patient_id,
        "priority_level": data.proposed_priority,
        "approved_by": data.clinician_name,
        "rationale": data.rationale,
        "status": "QUEUE_COMMITTED"
    }
    
    with open(LOCAL_DB_PATH, "r+") as f:
        db = json.load(f)
        db["logs"].append(entry)
        db["queue"].append({"patient_id": data.patient_id, "priority": data.proposed_priority})
        f.seek(0)
        json.dump(db, f, indent=4)
        f.truncate()
        
    return f"SUCCESS: Priority [{data.proposed_priority}] committed by {data.clinician_name} at {timestamp}."

if __name__ == "__main__":
    app.run()
