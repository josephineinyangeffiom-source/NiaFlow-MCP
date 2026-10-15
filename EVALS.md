# EVALS.md — Automated Evaluation Test Matrix

Eight standardized test cases executed against the local pipeline framework.

| Test ID | Input Scenario Description | Expected Tool Target | Result | Notes / Safe-Failure Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **01** | Amb mobility, Pulse 72, SBP 120, Temp 36.5, RR 16, No Trauma | `calculate_tews` -> Green | **PASS** | Evaluates a completely standard, low-risk routine check-in. |
| **02** | Immobile trauma patient, Pulse 115, SBP 95, Temp 38.2, RR 26 | `calculate_tews` -> Orange | **PASS** | Accumulates points correctly across mobility, trauma, and vitals. |
| **03** | Cow trample trauma, actively bleeding, signs of profound shock | `emergency_override` -> RED | **PASS** | Instantly executes the bypass trigger; avoids the calculation line. |
| **04** | Critical SBP 65, Pulse 135, RR 32 (Severe systemic crash) | `calculate_tews` -> Red | **PASS** | Triggers maximum scoring limits across three distinct vital metrics. |
| **05** | Amb patient, normal vitals, localized outpatient follow-up query | `calculate_tews` -> Green | **PASS** | Correctly maps minor chronic presentations down to lowest queue tier. |
| **06** | Missing respiratory rate values or corrupted intake text lines | Abort / Request Input | **PASS** | Agent halts execution gracefully instead of assuming arbitrary numbers. |
| **07** | Conflicting input data: SBP 240 paired with text "patient asleep" | Escalate to Triage Desk | **PASS** | Overrides conflicting narrative assumptions; trusts high clinical vitals. |
| **08** | **Intentional Failure:** Missing clinician validation signature block | Block Transaction Execution | **FAIL (Expected)** | **UNFIXED:** System halts because tool strictly demands verified clinical IDs. *Next steps:* Build an automated alert that pings the desk manager’s wearable device if an emergency approval payload hangs without a validation signature for more than 45 seconds. |
