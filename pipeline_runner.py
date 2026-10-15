import json
from smolagents import CodeAgent, Tool, LiteLLMEngine
from server import calculate_tews_score, emergency_clinical_override, stage_human_approval

class TewsCalculatorTool(Tool):
    name = "calculate_tews_score"
    description = "Computes deterministic SATS Triage Early Warning Score from raw integers."
    inputs = {
        "vitals": {"type": "object", "description": "Dict containing sbp, pulse, temp, rr, mobility, trauma"}
    }
    output_type = "any"
    def forward(self, vitals: dict) -> dict:
        return calculate_tews_score(vitals)

class EmergencyOverrideTool(Tool):
    name = "emergency_clinical_override"
    description = "Bypasses wait times instantly for life-threatening acute traumas."
    inputs = {
        "patient_id": {"type": "string", "description": "Unique patient identifier"},
        "trigger_complaint": {"type": "string", "description": "Raw string presentation text"}
    }
    output_type = "any"
    def forward(self, patient_id: str, trigger_complaint: str) -> dict:
        return emergency_clinical_override(patient_id, trigger_complaint)

class HumanApprovalGateTool(Tool):
    name = "stage_human_approval"
    description = "Irreversible Action Gate: Persists clinical decisions with a nurse's name sign-off."
    inputs = {
        "payload": {"type": "object", "description": "Dict with patient_id, proposed_priority, rationale, clinician_name"}
    }
    output_type = "string"
    def forward(self, payload: dict) -> str:
        return stage_human_approval(payload)

agent = CodeAgent(
    tools=[TewsCalculatorTool(), EmergencyOverrideTool(), HumanApprovalGateTool()],
    model=LiteLLMEngine(model_id="ollama/llama3.1:8b", api_base="http://localhost:11434"),
    add_base_tools=False
)

def run_triage_simulation():
    print("======================================================================")
    print("🚨 NIAFLOW-MCP SIMULATION: PROCESSING HIGH-URGENCY OUTPATIENT INTAKE")
    print("======================================================================\n")

    patient_id = "UCTH-ER-2026-001"
    complaint = "20-year-old male rushed into the ER after being violently trampled by a cow. Profound traumatic shock."
    
    print(f"[Intake Data Logged]: Processing Patient {patient_id}")
    print(f"[Presenting Complaint]: '{complaint}'\n")

    print("🔄 [Agent Action]: Checking critical life-threat indicators...")
    override_result = emergency_clinical_override(patient_id, complaint)
    print(f"📊 [Tool Output]: {json.dumps(override_result, indent=2)}\n")

    if override_result.get("action") == "IMMEDIATE_RED_BYPASS":
        print("🚨 CRITICAL LIFE THREAT DETECTED. BYPASSING STANDARD QUEUE FLOWS.")
        
        approval_payload = {
            "patient_id": patient_id,
            "proposed_priority": override_result["priority"],
            "rationale": f"Bypass triggered by critical trauma: {complaint}",
            "clinician_name": "Nurse Effiom (UCTH ER Triage Desk)"
        }
        
        print(f"✍️ [Gatekeeper Action]: Staging payload for verification by Nurse {approval_payload['clinician_name']}...")
        log_confirmation = stage_human_approval(approval_payload)
        print(f"\n💾 [Persistent Log Locked]: {log_confirmation}")
        print("\nQueue updated successfully. Patient isolated from paperwork delays.")

if __name__ == "__main__":
    run_triage_simulation()
