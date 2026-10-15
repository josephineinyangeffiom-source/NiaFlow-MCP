# ARCHITECTURE.md — NiaFlow-MCP

### 1. Agent Topology & Orchestration
NiaFlow-MCP uses a single-agent router pattern implemented with **smolagents / Pydantic AI**. The system separates the language reasoning layer from the clinical execution layer to completely eliminate LLM mathematical reasoning errors:
- **LLM Context Boundary:** The open-weights model (**Llama 3.1 8B / Qwen 2.5 7B**) reads unformatted, chaotic triage entries (including pidgin or localized emergency complaints). It extracts variables but is prohibited from deciding priority scores directly.
- **Data Sovereignty:** Operating entirely via a local **Ollama** runtime within Nigeria, fulfilling data residency rules. No PHI transits foreign APIs.

### 2. MCP Implementations (Built vs. Borrowed)
- **Built Server (Custom):** `NiaFlow-MCP` exposes deterministic clinical parsing structures (`calculate_tews_score`), a low-latency administrative emergency trigger tool (`emergency_clinical_override`), and an isolated compliance gate (`stage_human_approval`).
- **Borrowed Server:** The official community **File System MCP Server**.
  - *Why it beats writing it yourself:* Rather than inventing custom, fragile I/O methods to stream state changes across secondary clinic boundaries, using the validated community file server isolates local state preservation securely while allowing developers to focus purely on medical validation safety logic.

### 3. State Preservation Execution Graph
[Client Intake] ──> [LLM Extraction] ──> [MCP Clinical Validation Call] ──> [Human Validation Approval Gate] ──> [Local JSON State Update]
