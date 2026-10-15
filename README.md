# NiaFlow-MCP: Localized Triage & Data-Compliant Routing Architecture

NiaFlow-MCP is an open-source, data-sovereign triage routing infrastructure engineered to empower **overwhelmed, short-staffed triage nurses** and save lives in West African healthcare facilities.

---

## 🏥 1. Problem Statement
In West African public hospitals, the core bottleneck occurs where manual Outpatient Department (OPD) lines collide with high-stress Emergency Units. Triage lines remain paper-based even when basic billing bio-data is digital. Understaffed nurses face crushing multi-patient surges with zero decision support or automated tools to parse unstructured regional dialects. Consequently, acute patients sit behind routine clipboards, causing preventable deaths right on the waiting room floor. Furthermore, rural State Primary Health Centres (PHCs) run entirely on manual paper case cards, which are routinely lost during facility transfers, causing catastrophic medication and routing errors.

## 🌍 2. Solution Overview
NiaFlow-MCP acts as a localized digital bridge between manual intake lines and existing hospital registries. Operating on-premise via the Model Context Protocol (MCP), the agent reads raw intake complaints in English, Pidgin, or native dialects. If an acute threat is identified during a multi-patient surge, it activates an **Emergency Clinical Override** to fast-track the patient straight to the Emergency Unit. For stable cases, it calculates a mathematical Triage Early Warning Score (TEWS) grounded in the South African Triage Scale (SATS). It prevents fatal data loss by logging the validated triage data into a persistent local file log.

## 👥 3. Target Users
*   **Triage Nurses / Emergency Clinicians:** Overwhelmed frontline staff in understaffed public outpatient departments and emergency reception bays.
*   **Health Information Managers (HIM):** Officers requiring secure, auditable, and immutable local digital patient logs across fragmented secondary care networks.

---

## 🏗️ 4. Architecture & Data Flow
NiaFlow-MCP uses a single-agent router pattern that completely separates text reasoning from deterministic medical arithmetic, entirely eliminating LLM hallucinations.

[Raw Intake: Dialect/Pidgin] ──> [smolagents Client] ──> [NiaFlow-Core MCP Server] ──> [Human Validation Gate] ──> [Local JSON Ledger]

## 🛠️ 5. Technology Stack
*   **Agent Framework:** `smolagents` & `pydantic-ai` (Open-source orchestration)
*   **Local Inference Engine:** Ollama / vLLM (Air-gapped; 100% data sovereign)
*   **LLM Model:** `Llama-3.1-8B-Instruct` / `Qwen-2.5-7B-Instruct`
*   **Protocol Core:** FastMCP Python SDK (`mcp`)
*   **Data Persistence:** Local JSON Flat-File Architecture

---

## 🤖 6. Agent Architecture & MCP Implementation
The `smolagents` layer acts as the **MCP Client**. Upon initialization, it reads structural JSON schemas exposed by our servers and binds them dynamically as tools. 
*   **Custom Server (`NiaFlow-Core`):** Built with `FastMCP` to isolate strict clinical logic from the LLM core.
*   **Borrowed Server:** Integrated the community **File System MCP Server** to manage safe file read/write handles. This shields patient data within local network boundaries, avoiding custom, fragile database scripts.

## 🔧 7. MCP Tools & Servers
1.  `emergency_clinical_override` (Custom): Scans unformatted strings for critical **ABC (Airway, Breathing, Circulation)** distress parameters to bypass paperwork queues instantly.
2.  `calculate_tews_score` (Custom): Receives vitals and computes deterministic SATS/TEWS tiers using absolute Python arithmetic.
3.  `stage_human_approval` (Custom): Enforces the human signature requirement before logging.

## 🤝 8. Human-in-the-Loop Workflow
The agent is entirely restricted from making clinical diagnoses or autonomously modifying the live registry queue. It packages its recommendations into a structured verification payload and pauses execution. The system remains completely frozen at a **Human-in-the-Loop Validation Gate** until an attending clinician input validation block registers a named signature.

---

## 🚀 9. Setup & Installation Instructions
Run this single command string in your local terminal workspace to pull dependencies, configure variables, and run the triage suite pipeline:
```bash
pip install mcp pydantic smolagents && python pipeline_runner.py
```

## 📋 10. Usage Instructions
1.  Launch the script framework locally.
2.  Input raw triage presentation text or vital arrays when prompted by the intake parser interface.
3.  Observe the terminal execution trace as the agent calls the appropriate localized MCP tool.
4.  Input the clinical supervisor's name signature block to officially commit and log the transaction to disk.

---

## ⚠️ 11. Limitations
*   **Model Parameter Constraints:** Highly dependent on local hardware performance capacities to process dense open-weights multilingual weights smoothly at the edge.
*   **Static Local Schema:** Currently reads from a local directory JSON file block instead of a distributed network relational database cluster.

## 🔮 12. Future Improvements
*   **Wearable Trigger Alerts:** Integrate real-time automated messaging hooks to alert the ER clinical coordinator’s wearable smart device if an emergency payload sits waiting at the validation desk for more than 45 seconds.
*   **Federated Peer Registries:** Build a local area mesh network layer to safely synchronize specialist registry availability data between rural State PHCs and urban Federal Secondary facilities without cloud connectivity.
