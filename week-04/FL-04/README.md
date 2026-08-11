# FlyRank FL-04 — Governed Email Automation Workflow v2

> **Voice Card**: *"direct, technical, precise, metrics-driven, zero fluff"*

## Overview
**FL-04** is an 11-stage governed email drafting pipeline built for the FlyRank AI Internship (Week 4). It transforms raw natural language text requests into factual, high-specificity email drafts using structured JSON validation, dynamic quality gating, factual integrity auditing, and mandatory human oversight.

---

## Safety & Governance Guarantee
> **CRITICAL INVARIANT**: **`email_sent == False` across 100% of execution paths.**
> The system NEVER transmits emails automatically. Stage 11 mandates explicit human review (`APPROVED`, `EDITED`, or `REJECTED`) and outputs structured draft packages without outbound network transmission.

---

## 11-Stage Workflow Architecture

```
Stage 1: Input Acquisition ──────► Captures raw user input string
Stage 2: Type Classification ────► Categorizes email (Professor / Internship / Job App)
Stage 3: Requirements Loader ───► Dynamic schema loading (Mandatory vs Optional)
Stage 4: Extraction & Validation ─► Structured fact extraction & validation
Stage 5: Confirmation Gate 1 ────► User fact confirmation (Blocks if mandatory missing)
Stage 6: Draft Generator ────────► Grounded draft generation (Zero placeholders)
Stage 7: Critique Evaluator ─────► 5-criterion quality scoring (Specificity: 100)
Stage 8: Revision Engine ────────► Fact restoration & refinement (Capped at 5 attempts)
Stage 9: Fact Check Auditor ─────► Factual integrity audit & instant rollback engine
Stage 10: Final Quality Gate ─────► 8-criterion gate (Triggers SPECIAL_ATTENTION on fail)
Stage 11: Human Review Gate ─────► Mandatory human approval gate (email_sent=False)
```

---

## Current Verification & Audit Status

```text
Test Scenarios Executed: 10/10 (100% PASSED)
System Invariants Audit: 14/14 (100% PASSED)
Zero Email Sent Invariant: CONFIRMED (email_sent == False)
Real-Input Evaluation Runs: 5/5 PASSED
Execution Engine: Offline Semantic Fallback Engine (Keyless local testing mode)
Offline Measured Exec Time: ~0.0011s (Python orchestrator latency)
Projected Live API Exec Time: ~50.0s (~10s per run across 5 LLM stages)
Projected Time Reduction: ~87.1% estimated net time saved
```

> **Evaluation Disclaimer**:
> The five-run evaluation validated the workflow's orchestration, governance, failure handling, and human-review behavior. Because no LLM API key was available in the evaluation environment, the recorded execution timings represent the offline orchestration layer rather than live model inference. Manual drafting times are estimates, so live end-to-end time savings remain a projection rather than an empirical measurement.

---

## Quick Start & Usage

### 1. Run Final Integration Test Suite
```bash
python week-04/FL-04/tests/test_final_verification.py
```

### 2. Run Five Real-Input Evaluation Suite
```bash
python week-04/FL-04/run_real_evaluations.py
```

---

## Example Input & Expected Output

### Input
```text
I need to email my professor, Dr. Ahmed, asking for a 2-day extension on my Machine Learning assignment. The assignment is due tomorrow. I have been dealing with a family emergency and have not been able to complete it on time. Please ask politely if I can submit it two days late.
```

### Output Package (Stage 11 Human Review Gate)
```json
{
  "email_type": "Professor",
  "confirmed_facts": {
    "course_name": "Machine Learning",
    "assignment_name": "Machine Learning Assignment",
    "reason_for_delay": "Family emergency",
    "requested_extension_duration": "2 days",
    "professor_name": "Dr. Ahmed"
  },
  "current_draft": {
    "recipient": "Dr. Ahmed",
    "subject": "[Machine Learning] Extension Request: Machine Learning Assignment",
    "body_text": "Dear Dr. Ahmed,\n\nI am a student in Machine Learning. I missed Machine Learning Assignment due to family emergency and would like to request a 2-day extension.\n\nPlease let me know if granting a 2-day extension is possible. Thank you for your time and consideration.\n\nBest regards,"
  },
  "fact_check_passed": true,
  "quality_status": "FINAL_APPROVAL",
  "human_decision": "APPROVED",
  "workflow_complete": true,
  "email_sent": false
}
```

---

## Repository Structure
```text
week-04/
└── FL-04/
    ├── README.md                      # Project overview & audit status
    ├── walkthrough.md                 # Complete 21-section technical evaluation walkthrough
    ├── workflow_skeleton.py           # 11-stage pipeline orchestrator & state engine
    ├── llm_client.py                  # Structured JSON LLM client & fallback engine
    ├── run_real_evaluations.py        # 5 real-input evaluation runner & timing script
    ├── real_evaluations_results.json  # Telemetry results from 5 real evaluation runs
    └── tests/
        ├── test_final_verification.py   # Final 10-test & 14-invariant verification suite
        └── test_full_cycle_integration.py # Full-cycle integration tests
```
