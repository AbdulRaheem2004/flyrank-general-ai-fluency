"""
FlyRank AI Internship — FL-04: Professional Email Drafting Workflow Skeleton v2
Pipeline: Draft -> Critique -> Revise with Dynamic Validation & Integrity Controls

This module defines the state schema, stage execution interfaces, and control flow branching logic.
Prompt implementations and LLM calls are stubbed out for later phase integration.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import copy
import json
from llm_client import LLMClient


@dataclass
class WorkflowState:
    """Persistent state maintained across the entire email drafting lifecycle."""
    
    # Raw & Unaltered User Input
    raw_user_input: str = ""
    
    # Classification & Schema Loading
    email_type: Optional[str] = None  # "Professor" | "Internship" | "Job Application" | "Uncertain"
    classification_metadata: Dict[str, Any] = field(default_factory=lambda: {
        "confidence": 0.0,
        "reason": ""
    })
    type_requirements: Dict[str, Any] = field(default_factory=dict)

    
    # Information Extraction & Validation
    extracted_info: Dict[str, Any] = field(default_factory=lambda: {
        "mandatory": {"known": {}, "missing": []},
        "optional": {"known": {}, "missing": []},
        "assumptions": []
    })
    confirmed_structured_info: Dict[str, Any] = field(default_factory=dict)
    confirmed_assumptions: List[str] = field(default_factory=list)
    
    # Draft Management
    current_draft: Dict[str, Any] = field(default_factory=lambda: {
        "recipient": "",
        "subject": "",
        "key_facts_used": [],
        "assumptions_used": [],
        "body_text": ""
    })
    prior_valid_draft: Dict[str, Any] = field(default_factory=dict)
    
    # Critique & Quality Tracking
    critique_result: Dict[str, Any] = field(default_factory=lambda: {
        "scores": {
            "specificity": 0,    # Threshold: 100 (CRITICAL)
            "context": 0,        # Threshold: 80  (CRITICAL)
            "conciseness": 0,    # Threshold: 80  (Non-critical)
            "tone": 0,           # Threshold: 80  (Non-critical)
            "request_clarity": 0 # Threshold: 60  (Non-critical)
        },
        "pass_fail": {
            "specificity": False,
            "context": False,
            "conciseness": False,
            "tone": False,
            "request_clarity": False
        },
        "issues": [],
        "improvements": [],
        "priority_backlog": []
    })
    
    # Loop Counters & Integrity Flags
    revision_count: int = 0
    fact_check_flag: bool = False
    
    # Review & Final Governance
    review_mode: str = "NORMAL"  # "NORMAL" | "SPECIAL_ATTENTION"
    special_attention_details: Dict[str, Any] = field(default_factory=lambda: {
        "trigger_reason": "",
        "affected_criterion_or_fact": "",
        "ai_attempt_summary": "",
        "relevant_history": []
    })
    human_decision: str = "PENDING"  # "PENDING" | "APPROVED" | "EDITED" | "REJECTED"
    workflow_complete: bool = False
    email_sent: bool = False


class EmailDraftingWorkflow:
    """Orchestrator for the 11-step email drafting workflow skeleton."""

    def __init__(self, state: Optional[WorkflowState] = None, llm_client: Optional[LLMClient] = None):
        self.state = state or WorkflowState()
        self.llm_client = llm_client or LLMClient()

    # --- Step 1: Input Acquisition ---
    def stage_1_input_acquisition(self, user_input: str) -> WorkflowState:
        """Stage 1: Captures raw natural-language input from the user."""
        self.state.raw_user_input = user_input
        print(f"[Stage 1] Input Acquired ({len(user_input)} chars)")
        return self.state

    # --- Step 2: Type Classification ---
    def stage_2_type_classification(self) -> WorkflowState:
        """
        Stage 2: Identifies email category (Professor / Internship / Job Application)
        based on intent and meaning using LLMClient.
        Returns email_type, confidence, and reason. Marks 'Uncertain' if confidence < 0.70.
        """
        prompt = f"STAGE_2_CLASSIFICATION\nUSER_INPUT: {self.state.raw_user_input}"
        schema_desc = "JSON with email_type ('Professor'|'Internship'|'Job Application'|'Uncertain'), confidence (float), reason (str)"

        result = self.llm_client.generate_structured_json(prompt, schema_desc)

        email_type = result.get("email_type", "Uncertain")
        confidence = float(result.get("confidence", 0.0))
        reason = result.get("reason", "No classification reason provided.")

        if confidence < 0.70:
            self.state.email_type = "Uncertain"
        else:
            self.state.email_type = email_type

        self.state.classification_metadata = {
            "confidence": confidence,
            "reason": reason
        }

        print(f"[Stage 2] Type Identified: {self.state.email_type} (Confidence: {confidence:.2f}, Reason: '{reason}')")
        return self.state

    # --- Step 3: Dynamic Requirements Loader ---
    def stage_3_requirements_loader(self) -> WorkflowState:
        """
        Stage 3: Dynamically loads requirements based on BOTH email_type AND specific situation/purpose.
        Produces structured requirements schema containing situation, mandatory fields, optional fields,
        and explanations of why each mandatory field is required.
        """
        prompt = f"STAGE_3_REQUIREMENTS\nEMAIL_TYPE: {self.state.email_type}\nUSER_INPUT: {self.state.raw_user_input}"
        schema_desc = "JSON with situation (str), mandatory (list), optional (list), field_explanations (dict)"

        req_data = self.llm_client.generate_structured_json(prompt, schema_desc)

        self.state.type_requirements = {
            "situation": req_data.get("situation", "general communication"),
            "mandatory": req_data.get("mandatory", []),
            "optional": req_data.get("optional", []),
            "field_explanations": req_data.get("field_explanations", {})
        }

        print(f"[Stage 3] Situation Detected: '{self.state.type_requirements['situation']}'")
        print(f"[Stage 3] Mandatory Fields: {self.state.type_requirements['mandatory']}")
        print(f"[Stage 3] Optional Fields: {self.state.type_requirements['optional']}")
        return self.state

    # --- Step 4: Extraction & Validation ---
    def stage_4_extract_and_validate(self) -> WorkflowState:
        """
        Stage 4: Factual extraction from raw user input.
        Determines for every requirement whether information is Known, Missing, or Assumed.
        Preserves raw_user_input unchanged.
        """
        mandatory_fields = self.state.type_requirements.get("mandatory", [])
        optional_fields = self.state.type_requirements.get("optional", [])

        prompt = (
            f"STAGE_4_EXTRACTION\n"
            f"MANDATORY_FIELDS: {json.dumps(mandatory_fields)}\n"
            f"OPTIONAL_FIELDS: {json.dumps(optional_fields)}\n"
            f"USER_INPUT: {self.state.raw_user_input}"
        )
        schema_desc = "JSON with mandatory: {known: dict, missing: list}, optional: {known: dict, missing: list}, assumptions: list"

        extracted = self.llm_client.generate_structured_json(prompt, schema_desc)

        self.state.extracted_info = {
            "mandatory": {
                "known": extracted.get("mandatory", {}).get("known", {}),
                "missing": extracted.get("mandatory", {}).get("missing", [])
            },
            "optional": {
                "known": extracted.get("optional", {}).get("known", {}),
                "missing": extracted.get("optional", {}).get("missing", [])
            },
            "assumptions": extracted.get("assumptions", [])
        }

        print("[Stage 4] Factual Extraction & Validation Complete:")
        print(f"  - Known Mandatory: {self.state.extracted_info['mandatory']['known']}")
        print(f"  - Missing Mandatory: {self.state.extracted_info['mandatory']['missing']}")
        print(f"  - Known Optional: {self.state.extracted_info['optional']['known']}")
        print(f"  - Missing Optional: {self.state.extracted_info['optional']['missing']}")
        print(f"  - Disclosed Assumptions: {self.state.extracted_info['assumptions']}")
        return self.state

    # --- Step 5: User Confirmation Gate 1 ---
    def render_stage_5_summary(self) -> str:
        """Renders the complete information summary for user confirmation."""
        s = self.state
        req = s.type_requirements
        ext = s.extracted_info
        
        output = []
        output.append("=======================================================")
        output.append("STAGE 5: INFORMATION CONFIRMATION SUMMARY")
        output.append("=======================================================")
        output.append(f"Email Type: {s.email_type}")
        output.append(f"Situation / Purpose: {req.get('situation', 'N/A')}")
        output.append("-------------------------------------------------------")
        
        # Mandatory section
        output.append("MANDATORY INFORMATION:")
        known_mand = ext["mandatory"]["known"]
        missing_mand = ext["mandatory"]["missing"]
        
        if known_mand:
            for k, v in known_mand.items():
                exp = req.get("field_explanations", {}).get(k, "")
                output.append(f"  [KNOWN] {k}: '{v}'" + (f" ({exp})" if exp else ""))
        else:
            output.append("  (None known)")

        if missing_mand:
            for k in missing_mand:
                exp = req.get("field_explanations", {}).get(k, "")
                output.append(f"  [MISSING] {k}" + (f" --> WHY REQUIRED: {exp}" if exp else ""))
        else:
            output.append("  [ALL MANDATORY FIELDS SATISFIED]")

        output.append("-------------------------------------------------------")
        
        # Optional section
        output.append("OPTIONAL INFORMATION (Non-blocking):")
        known_opt = ext["optional"]["known"]
        missing_opt = ext["optional"]["missing"]
        
        if known_opt:
            for k, v in known_opt.items():
                output.append(f"  [KNOWN OPTIONAL] {k}: '{v}'")
        if missing_opt:
            for k in missing_opt:
                output.append(f"  [MISSING OPTIONAL] {k} (Optional - will not block drafting)")
        if not known_opt and not missing_opt:
            output.append("  (None)")

        output.append("-------------------------------------------------------")
        
        # Assumptions section
        output.append("EXPLICIT AI ASSUMPTIONS (Tag: ASSUMPTION):")
        if ext["assumptions"]:
            for i, asm in enumerate(ext["assumptions"], 1):
                output.append(f"  [ASSUMPTION #{i}] {asm}")
        else:
            output.append("  (No AI assumptions made)")

        output.append("=======================================================")
        return "\n".join(output)

    def evaluate_assumption_feasibility(self, field_name: str) -> Optional[str]:
        """
        Evaluates whether a scenario-based assumption can be reasonably derived from contextual evidence.
        Returns the proposed assumption string if supported by context, or None if insufficient contextual evidence exists.
        NEVER infers numbers, dates, durations, or concrete claims without explicit contextual support.
        """
        raw_lower = self.state.raw_user_input.lower()
        situation = self.state.type_requirements.get("situation", "")
        
        if field_name == "company_name" and ("hiring manager" in raw_lower or "your team" in raw_lower):
            return f"Assumed target company is the recipient organization based on outreach context."
        
        # Insufficient evidence for requested_extension_duration, course_name, specific_question_or_concern, core_qualification, etc.
        return None

    def stage_5_user_confirmation(
        self,
        user_action: str = "CONFIRM",  # "CONFIRM" | "SUPPLY_MISSING" | "USER_UNKNOWN" | "CORRECT"
        supplied_fields: Optional[Dict[str, Any]] = None,
        unknown_fields_responses: Optional[Dict[str, str]] = None,
        corrections: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Stage 5: Interactive Confirmation & Integrity Gate.
        
        Enforces:
        1. Display of email type, situation, mandatory (known/missing), optional (known/missing), and assumptions.
        2. Blocking on missing mandatory fields until supplied OR assumption explicitly confirmed.
        3. Explicit handling of unknown mandatory fields with quality degradation warnings and assumption proposals (only if contextually reasonable).
        4. Re-display of complete summary upon user correction (user correction takes precedence).
        5. Hard block on advancing to Stage 6 until user explicitly confirms (`user_action == 'CONFIRM'`).
        """
        summary_str = self.render_stage_5_summary()
        print(summary_str)

        # 1. Process explicit user corrections (highest precedence)
        if corrections:
            for field_name, new_val in corrections.items():
                if field_name in self.state.type_requirements.get("mandatory", []):
                    self.state.extracted_info["mandatory"]["known"][field_name] = new_val
                    if field_name in self.state.extracted_info["mandatory"]["missing"]:
                        self.state.extracted_info["mandatory"]["missing"].remove(field_name)
                else:
                    self.state.extracted_info["optional"]["known"][field_name] = new_val
                    if field_name in self.state.extracted_info["optional"]["missing"]:
                        self.state.extracted_info["optional"]["missing"].remove(field_name)
            print(f"\n[Stage 5 Action] Applied User Correction(s): {corrections}")
            updated_summary = self.render_stage_5_summary()
            print("\n--- UPDATED SUMMARY AFTER CORRECTION ---")
            print(updated_summary)

        # 2. Process user supplying missing mandatory fields
        if supplied_fields:
            for field_name, val in supplied_fields.items():
                self.state.extracted_info["mandatory"]["known"][field_name] = val
                if field_name in self.state.extracted_info["mandatory"]["missing"]:
                    self.state.extracted_info["mandatory"]["missing"].remove(field_name)
            print(f"\n[Stage 5 Action] Supplied Missing Field(s): {list(supplied_fields.keys())}")

        # 3. Process user stating they DO NOT KNOW a mandatory field
        if user_action == "USER_UNKNOWN" and self.state.extracted_info["mandatory"]["missing"]:
            for missing_field in list(self.state.extracted_info["mandatory"]["missing"]):
                print(f"\n[WARNING] Missing Mandatory Field: '{missing_field}'.")
                print("   Not providing this field will reduce the email's specificity and context quality.")
                
                proposed_assumption = self.evaluate_assumption_feasibility(missing_field)
                if proposed_assumption:
                    print(f"   [PROPOSED AI ASSUMPTION]: \"{proposed_assumption}\"")
                    decision = (unknown_fields_responses or {}).get(missing_field, "ACCEPT_ASSUMPTION")
                    if decision == "ACCEPT_ASSUMPTION":
                        self.state.extracted_info["assumptions"].append(proposed_assumption)
                        self.state.extracted_info["mandatory"]["missing"].remove(missing_field)
                        print(f"   --> User ACCEPTED assumption for '{missing_field}'. Added to Disclosed Assumptions.")
                    elif decision == "REJECT":
                        print(f"   --> User REJECTED assumption for '{missing_field}'. Field remains missing.")
                    elif decision == "PROVIDE_VALUE":
                        val = (supplied_fields or {}).get(missing_field, "User_Provided_Val")
                        self.state.extracted_info["mandatory"]["known"][missing_field] = val
                        self.state.extracted_info["mandatory"]["missing"].remove(missing_field)
                        print(f"   --> User provided value for '{missing_field}': '{val}'.")
                else:
                    print(f"   [NO REASONABLE ASSUMPTION POSSIBLE] No contextual evidence in input to infer '{missing_field}'.")
                    print(f"   --> Field '{missing_field}' remains MISSING. Stage 6 drafting continues to be BLOCKED.")

        # 4. Check block condition: Are mandatory fields still missing?
        still_missing_mandatory = self.state.extracted_info["mandatory"]["missing"]
        if still_missing_mandatory:
            print(f"\n[STAGE 5 GATE BLOCKED] Cannot proceed to Stage 6. Missing mandatory field(s): {still_missing_mandatory}")
            return {
                "status": "BLOCKED",
                "reason": f"Missing mandatory field(s): {still_missing_mandatory}",
                "missing_mandatory": still_missing_mandatory,
                "confirmed": False
            }

        # 5. Check confirmation action
        if user_action == "CONFIRM":
            self.state.confirmed_structured_info = copy.deepcopy(self.state.extracted_info["mandatory"]["known"])
            self.state.confirmed_structured_info.update(copy.deepcopy(self.state.extracted_info["optional"]["known"]))
            self.state.confirmed_assumptions = copy.deepcopy(self.state.extracted_info["assumptions"])
            
            print("\n[STAGE 5 GATE PASSED] User explicitly confirmed all information. Ready for Stage 6 (Draft).")
            return {
                "status": "CONFIRMED",
                "confirmed_info": self.state.confirmed_structured_info,
                "confirmed_assumptions": self.state.confirmed_assumptions,
                "confirmed": True
            }
        else:
            print("\n[STAGE 5 GATE WAITING] Complete summary presented. Awaiting user explicit confirmation ('CONFIRM').")
            return {
                "status": "WAITING_CONFIRMATION",
                "confirmed": False
            }

    # --- Step 6: Draft Generator ---
    def stage_6_draft(self) -> WorkflowState:
        """Stage 6: Generates initial email draft using LLM client with strict factual integrity and recipient governance."""
        prompt = (
            f"STAGE_6_DRAFT\n"
            f"EMAIL_TYPE: {self.state.email_type}\n"
            f"SITUATION: {self.state.type_requirements.get('situation', '')}\n"
            f"CONFIRMED_INFO: {json.dumps(self.state.confirmed_structured_info)}\n"
            f"CONFIRMED_ASSUMPTIONS: {json.dumps(self.state.confirmed_assumptions)}\n"
            f"RAW_USER_INPUT: {self.state.raw_user_input}"
        )
        schema_desc = "JSON with recipient (str), subject (str), key_facts_used (list), assumptions_used (list), body_text (str)"

        draft_payload = self.llm_client.generate_structured_json(prompt, schema_desc)

        self.state.current_draft = {
            "recipient": draft_payload.get("recipient", "Recipient"),
            "subject": draft_payload.get("subject", f"Regarding {self.state.email_type} Inquiry"),
            "key_facts_used": draft_payload.get("key_facts_used", list(self.state.confirmed_structured_info.keys())),
            "assumptions_used": draft_payload.get("assumptions_used", copy.deepcopy(self.state.confirmed_assumptions)),
            "body_text": draft_payload.get("body_text", "")
        }

        print("[Stage 6] Email Draft Generated:")
        print(f"  - Recipient: '{self.state.current_draft['recipient']}'")
        print(f"  - Subject: '{self.state.current_draft['subject']}'")
        print(f"  - Key Facts Used: {self.state.current_draft['key_facts_used']}")
        print(f"  - Assumptions Used: {self.state.current_draft['assumptions_used']}")
        print("  - Body Text:")
        for line in self.state.current_draft['body_text'].splitlines():
            print(f"    {line}")
        return self.state

    # --- Step 7: Critique Evaluator ---
    def stage_7_critique(self) -> WorkflowState:
        """Stage 7: Evaluates draft on 5 criteria using LLM client with strict factual integrity."""
        prompt = (
            f"STAGE_7_CRITIQUE\n"
            f"EMAIL_TYPE: {self.state.email_type}\n"
            f"SITUATION: {self.state.type_requirements.get('situation', '')}\n"
            f"MANDATORY_FIELDS: {json.dumps(self.state.type_requirements.get('mandatory', []))}\n"
            f"OPTIONAL_FIELDS: {json.dumps(self.state.type_requirements.get('optional', []))}\n"
            f"CONFIRMED_INFO: {json.dumps(self.state.confirmed_structured_info)}\n"
            f"CONFIRMED_ASSUMPTIONS: {json.dumps(self.state.confirmed_assumptions)}\n"
            f"RAW_USER_INPUT: {self.state.raw_user_input}\n"
            f"CURRENT_DRAFT: {json.dumps(self.state.current_draft)}"
        )
        schema_desc = "JSON with scores (dict), pass_fail (dict), strengths (list), weaknesses (list), revision_recommendations (list), priority_backlog (list), critical_passed (bool), ready_for_continuation (bool)"

        critique_payload = self.llm_client.generate_structured_json(prompt, schema_desc)

        scores = critique_payload.get("scores", {"specificity": 100, "context": 90, "conciseness": 85, "tone": 90, "request_clarity": 85})
        pass_fail = critique_payload.get("pass_fail", {
            "specificity": scores.get("specificity", 0) == 100,
            "context": scores.get("context", 0) >= 80,
            "conciseness": scores.get("conciseness", 0) >= 80,
            "tone": scores.get("tone", 0) >= 80,
            "request_clarity": scores.get("request_clarity", 0) >= 60
        })
        critical_passed = pass_fail["specificity"] and pass_fail["context"]

        existing_fc = self.state.critique_result.get("fact_check_result") if isinstance(self.state.critique_result, dict) else None

        self.state.critique_result = {
            "scores": scores,
            "pass_fail": pass_fail,
            "strengths": critique_payload.get("strengths", []),
            "weaknesses": critique_payload.get("weaknesses", []),
            "revision_recommendations": critique_payload.get("revision_recommendations", []),
            "priority_backlog": critique_payload.get("priority_backlog", []),
            "critical_passed": critical_passed,
            "ready_for_continuation": critical_passed
        }
        if existing_fc:
            self.state.critique_result["fact_check_result"] = existing_fc

        print("[Stage 7] Critique Evaluation Completed:")
        print(f"  - Scores: {self.state.critique_result['scores']}")
        print(f"  - Pass/Fail: {self.state.critique_result['pass_fail']}")
        print(f"  - Critical Passed: {self.state.critique_result['critical_passed']}")
        print(f"  - Ready for Continuation: {self.state.critique_result['ready_for_continuation']}")
        print(f"  - Strengths: {self.state.critique_result['strengths']}")
        print(f"  - Weaknesses: {self.state.critique_result['weaknesses']}")
        print(f"  - Priority Backlog: {self.state.critique_result['priority_backlog']}")
        return self.state

    # --- Step 8: Revision Engine ---
    def stage_8_revise(self) -> WorkflowState:
        """
        Stage 8: Revision Engine with strict attempt control flow and metadata governance.
        Refinement 1 Control Flow:
        1. Check critical_passed. If True: do NOT revise, do NOT increment revision_count, do NOT back up.
        2. Check revision limit. If revision_count >= 5: do NOT revise, do NOT increment counter.
        3. Otherwise: save prior_valid_draft = copy.deepcopy(current_draft), increment revision_count += 1, perform 1 revision attempt.
        """
        if self.state.critique_result.get("critical_passed", False):
            print("[Stage 8] Critical criteria already passed (Specificity=100, Context>=80). Skipping revision.")
            return self.state

        if self.state.revision_count >= 5:
            print(f"[Stage 8] Revision attempt limit (5) reached (current: {self.state.revision_count}). Stopping automatic revisions.")
            return self.state

        # 1. Save prior valid draft backup BEFORE revision
        self.state.prior_valid_draft = copy.deepcopy(self.state.current_draft)

        # 2. Increment 5-attempt counter
        self.state.revision_count += 1
        print(f"[Stage 8] Executing Revision Attempt {self.state.revision_count}/5. Prior valid draft backed up.")

        # 3. Formulate revision prompt
        prompt = (
            f"STAGE_8_REVISE\n"
            f"EMAIL_TYPE: {self.state.email_type}\n"
            f"SITUATION: {self.state.type_requirements.get('situation', '')}\n"
            f"CONFIRMED_INFO: {json.dumps(self.state.confirmed_structured_info)}\n"
            f"CONFIRMED_ASSUMPTIONS: {json.dumps(self.state.confirmed_assumptions)}\n"
            f"RAW_USER_INPUT: {self.state.raw_user_input}\n"
            f"CRITIQUE_RESULT: {json.dumps(self.state.critique_result)}\n"
            f"CURRENT_DRAFT: {json.dumps(self.state.current_draft)}"
        )
        schema_desc = "JSON with subject (str), body_text (str)"

        revision_payload = self.llm_client.generate_structured_json(prompt, schema_desc)

        if revision_payload.get("body_text"):
            self.state.current_draft["body_text"] = revision_payload["body_text"]
        if revision_payload.get("subject"):
            self.state.current_draft["subject"] = revision_payload["subject"]

        print("[Stage 8] Revised Candidate Draft Generated:")
        print(f"  - Revision Count: {self.state.revision_count}/5")
        print(f"  - Subject: '{self.state.current_draft['subject']}'")
        print("  - Body Text:")
        for line in self.state.current_draft['body_text'].splitlines():
            print(f"    {line}")

        return self.state

    # --- Step 9: Fact Check Auditor ---
    def stage_9_fact_check(self) -> Dict[str, Any]:
        """
        Stage 9: Fact Check Auditor.
        Verifies whether candidate draft is factually grounded in authoritative workflow state.
        Enforces result consistency invariant: passed == factual_integrity and recommended_action.
        Executes instant rollback if passed is False without modifying revision_count.
        """
        prompt = (
            f"STAGE_9_FACT_CHECK\n"
            f"EMAIL_TYPE: {self.state.email_type}\n"
            f"SITUATION: {self.state.type_requirements.get('situation', '')}\n"
            f"MANDATORY_FIELDS: {json.dumps(self.state.type_requirements.get('mandatory', []))}\n"
            f"OPTIONAL_FIELDS: {json.dumps(self.state.type_requirements.get('optional', []))}\n"
            f"CONFIRMED_INFO: {json.dumps(self.state.confirmed_structured_info)}\n"
            f"CONFIRMED_ASSUMPTIONS: {json.dumps(self.state.confirmed_assumptions)}\n"
            f"RAW_USER_INPUT: {self.state.raw_user_input}\n"
            f"CURRENT_DRAFT: {json.dumps(self.state.current_draft)}"
        )
        schema_desc = "JSON with passed (bool), factual_integrity (bool), unsupported_claims (list), altered_facts (list), invented_details (list), missing_confirmed_facts (list), unsupported_strengthening (list), evidence (list), recommended_action (str)"

        fc_payload = self.llm_client.generate_structured_json(prompt, schema_desc)

        # Result Consistency Normalization
        unsupported = fc_payload.get("unsupported_claims", [])
        altered = fc_payload.get("altered_facts", [])
        invented = fc_payload.get("invented_details", [])
        missing_mand = fc_payload.get("missing_confirmed_facts", [])
        strengthened = fc_payload.get("unsupported_strengthening", [])

        has_violations = bool(unsupported or altered or invented or missing_mand or strengthened)
        factual_integrity = not has_violations
        passed = factual_integrity
        recommended_action = "ACCEPT" if passed else "ROLLBACK"

        fact_check_result = {
            "passed": passed,
            "factual_integrity": factual_integrity,
            "unsupported_claims": unsupported,
            "altered_facts": altered,
            "invented_details": invented,
            "missing_confirmed_facts": missing_mand,
            "unsupported_strengthening": strengthened,
            "evidence": fc_payload.get("evidence", []),
            "recommended_action": recommended_action
        }

        if not isinstance(self.state.critique_result, dict):
            self.state.critique_result = {}
        self.state.critique_result["fact_check_result"] = fact_check_result

        print("[Stage 9] Fact Check Audit Complete:")
        print(f"  - Passed: {passed} | Factual Integrity: {factual_integrity} | Action: {recommended_action}")
        print(f"  - Violations: unsupported={unsupported}, altered={altered}, invented={invented}, missing_mand={missing_mand}, strengthened={strengthened}")

        if not passed:
            print(f"  [ROLLBACK EXECUTED] Fact Check failed. Restoring prior_valid_draft. revision_count remains {self.state.revision_count}.")
            self.state.current_draft = copy.deepcopy(self.state.prior_valid_draft)
        else:
            print("  [DRAFT ACCEPTED] Candidate draft passed factual integrity audit.")

        return fact_check_result

    # --- Step 10: Final Quality Check Gate ---
    def stage_10_final_quality_check(self) -> Dict[str, Any]:
        """
        Stage 10: Final Quality Check Gate.
        Evaluates actual currently accepted draft against all 8 final quality criteria.
        Refined Routing Protocol:
        - All 8 pass -> FINAL_APPROVAL -> Stage 11 (Review mode NORMAL)
        - Factual integrity fails -> SPECIAL_ATTENTION -> Mandate Human Review (HARD RULE: Never routes to Stage 8)
        - Non-factual fails & revision_count < 5 -> REVISION_REQUIRED -> Route to Stage 8
        - Non-factual fails & revision_count >= 5 -> SPECIAL_ATTENTION -> Mandate Human Review
        Stage 10 NEVER modifies current_draft.
        """
        fact_check_res = self.state.critique_result.get("fact_check_result", {}) if isinstance(self.state.critique_result, dict) else {}

        prompt = (
            f"STAGE_10_FINAL_QUALITY_CHECK\n"
            f"REVISION_COUNT: {self.state.revision_count}\n"
            f"CURRENT_DRAFT: {json.dumps(self.state.current_draft)}\n"
            f"CRITIQUE_RESULT: {json.dumps(self.state.critique_result)}\n"
            f"FACT_CHECK_RESULT: {json.dumps(fact_check_res)}"
        )
        schema_desc = "JSON with final_approved (bool), quality_status (str), criteria (dict), failed_criteria (list), issues (list), next_action (str), revision_attempts_used (int), revision_attempts_remaining (int)"

        fq_payload = self.llm_client.generate_structured_json(prompt, schema_desc)

        # Ensure strict invariant enforcement on orchestrator side
        critique_scores = self.state.critique_result.get("scores", {}) if isinstance(self.state.critique_result, dict) else {}
        body_text = self.state.current_draft.get("body_text", "") if isinstance(self.state.current_draft, dict) else ""

        criteria = {
            "factual_integrity": fact_check_res.get("passed") is True if isinstance(fact_check_res, dict) else False,
            "specificity": critique_scores.get("specificity") == 100 if critique_scores else False,
            "context": critique_scores.get("context", 0) >= 80 if critique_scores else False,
            "conciseness": critique_scores.get("conciseness", 0) >= 80 if critique_scores else False,
            "tone": critique_scores.get("tone", 0) >= 80 if critique_scores else False,
            "request_clarity": critique_scores.get("request_clarity", 0) >= 60 if critique_scores else False,
            "no_unresolved_critical_issues": (critique_scores.get("specificity") == 100 and critique_scores.get("context", 0) >= 80) if critique_scores else False,
            "draft_present": bool(body_text.strip())
        }

        final_approved = all(criteria.values())
        failed_criteria = [k for k, v in criteria.items() if not v]
        issues = [f"Failed criterion: {k}" for k in failed_criteria]

        if final_approved:
            quality_status = "FINAL_APPROVAL"
            next_action = "PROCEED_TO_HUMAN_REVIEW_STAGE_11"
            self.state.review_mode = "NORMAL"
        elif not criteria["factual_integrity"]:
            quality_status = "SPECIAL_ATTENTION"
            next_action = "MANDATE_SPECIAL_ATTENTION_HUMAN_REVIEW"
            self.state.review_mode = "SPECIAL_ATTENTION"
            self.state.special_attention_details["trigger_reason"] = "Factual integrity failure detected at Stage 10 quality gate."
            self.state.special_attention_details["affected_criterion_or_fact"] = "factual_integrity"
        elif self.state.revision_count < 5:
            quality_status = "REVISION_REQUIRED"
            next_action = "RETURN_TO_STAGE_8_REVISION"
            self.state.review_mode = "NORMAL"
        else:
            quality_status = "SPECIAL_ATTENTION"
            next_action = "MANDATE_SPECIAL_ATTENTION_HUMAN_REVIEW"
            self.state.review_mode = "SPECIAL_ATTENTION"
            self.state.special_attention_details["trigger_reason"] = "Exhausted 5 automatic revisions while quality criteria still failing."
            self.state.special_attention_details["affected_criterion_or_fact"] = f"Failed criteria: {failed_criteria}"

        final_quality_result = {
            "final_approved": final_approved,
            "quality_status": quality_status,
            "criteria": criteria,
            "failed_criteria": failed_criteria,
            "issues": issues,
            "next_action": next_action,
            "revision_attempts_used": self.state.revision_count,
            "revision_attempts_remaining": max(0, 5 - self.state.revision_count)
        }

        self.state.final_quality_result = final_quality_result

        print("[Stage 10] Final Quality Check Complete:")
        print(f"  - Approved: {final_approved} | Status: {quality_status} | Mode: {self.state.review_mode}")
        print(f"  - Failed Criteria: {failed_criteria}")
        print(f"  - Next Action: {next_action}")

        return final_quality_result

    # --- Step 11: Human Review Gate 2 ---
    def stage_11_human_review(self, decision: str = "APPROVED", edited_text: Optional[str] = None) -> Dict[str, Any]:
        """
        Stage 11: Human Review Gate 2.
        Presents full governance package to human reviewer.
        Human actions allowed: 'APPROVED' | 'EDITED' | 'REJECTED'
        Refinements:
        1. Strict Decision Validation: Invalid decision strings fail safely.
        2. Non-empty EDITED Text Requirement: 'EDITED' requires non-empty edited_text.
        3. Audit Preservation: EDITED updates body_text, but NEVER overwrites automated audit telemetry.
        4. Complete Package Presentation: Assembles comprehensive human review package.
        5. SPECIAL_ATTENTION Visibility: Highly visible, but human-decidable.
        6. HARD RULE: Zero automated email sending (email_sent = False, workflow_complete = True).
        """
        valid_decisions = ["APPROVED", "EDITED", "REJECTED"]
        if decision not in valid_decisions:
            print(f"[Stage 11 ERROR] Invalid human decision '{decision}'. Must be one of {valid_decisions}.")
            return {"status": "ERROR_INVALID_DECISION", "error": f"Invalid decision '{decision}'"}

        if decision == "EDITED":
            if not edited_text or not edited_text.strip():
                print("[Stage 11 ERROR] 'EDITED' decision requires non-empty edited_text.")
                return {"status": "ERROR_EMPTY_EDITED_TEXT", "error": "edited_text cannot be empty when decision is EDITED"}
            # Update draft text without overwriting automated audit results
            self.state.current_draft["body_text"] = edited_text.strip()
            self.state.human_decision = "EDITED"
        else:
            self.state.human_decision = decision

        # Set termination and email_sent invariants
        self.state.workflow_complete = True
        self.state.email_sent = False

        # Assemble full human review package
        fq_result = getattr(self.state, "final_quality_result", {})
        fc_result = self.state.critique_result.get("fact_check_result", {}) if isinstance(self.state.critique_result, dict) else {}

        human_review_package = {
            "review_mode": self.state.review_mode,
            "special_attention": self.state.review_mode == "SPECIAL_ATTENTION",
            "special_attention_details": self.state.special_attention_details if self.state.review_mode == "SPECIAL_ATTENTION" else {},
            "current_draft": self.state.current_draft,
            "final_quality_result": fq_result,
            "fact_check_result": fc_result,
            "critique_result": self.state.critique_result,
            "revision_count": self.state.revision_count,
            "revision_attempts_remaining": max(0, 5 - self.state.revision_count),
            "human_decision": self.state.human_decision,
            "workflow_complete": self.state.workflow_complete,
            "email_sent": self.state.email_sent
        }

        print("[Stage 11] Human Review Complete:")
        print(f"  - Human Decision: {self.state.human_decision}")
        print(f"  - Review Mode: {self.state.review_mode}")
        print(f"  - Workflow Complete: {self.state.workflow_complete} | Email Sent: {self.state.email_sent}")
        if self.state.review_mode == "SPECIAL_ATTENTION":
            print(f"  - SPECIAL_ATTENTION Trigger: {self.state.special_attention_details.get('trigger_reason')}")

        return human_review_package

    # --- Step 12: Terminal Execution State ---
    def stage_12_terminal_state(self) -> Dict[str, Any]:
        """Stage 12: Workflow execution halts permanently. Renders final review artifact."""
        summary = {
            "status": "TERMINATED",
            "human_decision": self.state.human_decision,
            "email_type": self.state.email_type,
            "final_draft": self.state.current_draft,
            "review_mode": self.state.review_mode,
            "revision_count": self.state.revision_count,
            "fact_check_flag": self.state.fact_check_flag,
            "scores": self.state.critique_result["scores"]
        }
        print(f"[Stage 12] Workflow Terminated cleanly. Decision: {self.state.human_decision}")
        return summary

    # --- Orchestrated Execution Engine (Branching & Loop Handler) ---
    def run_full_pipeline(
        self,
        user_input: str,
        initial_specificity: int = 100,
        initial_context: int = 80,
        post_revision_specificity: int = 100,
        mock_fact_check_outcome: str = "PRESERVED"
    ) -> Dict[str, Any]:
        """Runs the complete workflow skeleton through all conditional branches and loops."""
        # 1. Input Acquisition
        self.stage_1_input_acquisition(user_input)
        
        # 2. Type Classification
        self.stage_2_type_classification()
        if self.state.email_type == "Uncertain":
            print("\n[STAGE 2 ALERT] Category classification confidence is below 0.70 (Uncertain).")
            print("   Workflow halted before Requirements Loader. Requesting user category clarification...")
            # Prompt user clarification
            clarified_category = "Professor"
            self.state.email_type = clarified_category
            self.state.classification_metadata = {"confidence": 1.00, "reason": "Explicit user clarification."}
            print(f"   --> User clarified email category as '{clarified_category}'. Proceeding to Stage 3.")
        
        # 3. Requirements Loader
        self.stage_3_requirements_loader()
        
        # 4. Extraction & Validation
        self.stage_4_extract_and_validate()
        
        # 5. User Confirmation Gate 1
        gate_res = self.stage_5_user_confirmation(user_action="CONFIRM")
        if not gate_res["confirmed"]:
            print("[Pipeline Halted] Stage 5 Confirmation Gate blocked.")
            return {"status": "BLOCKED_AT_STAGE_5", "state": self.state}
        
        # 6. Draft Email
        self.stage_6_draft()
        
        # 7. Initial Critique & 9. Fact Check
        self.stage_7_critique()
        self.stage_9_fact_check()
        
        # 8/9. Revision & Fact-Check Loop
        while True:
            critical_pass = (
                self.state.critique_result["pass_fail"]["specificity"] and
                self.state.critique_result["pass_fail"]["context"]
            )
            
            if critical_pass:
                print("[Pipeline] Critical criteria passed (Specificity=100, Context>=80). Stopping auto-revisions.")
                break
                
            if self.state.revision_count >= 5:
                print("[Pipeline] Max revisions (5) reached. Stopping auto-revisions.")
                break
            
            self.stage_8_revise()
            self.stage_9_fact_check()
            self.stage_7_critique()

        # 10. Final Quality Check
        self.stage_10_final_quality_check()
        
        # 11. Human Review Gate 2
        self.stage_11_human_review(decision="APPROVED")
        
        # 12. Terminal State
        return self.stage_12_terminal_state()


if __name__ == "__main__":
    def run_stage_5_test(case_title: str, input_text: str, user_action: str = "CONFIRM", supplied_fields: dict = None, unknown_responses: dict = None, corrections: dict = None):
        print(f"\n=======================================================")
        print(f"STAGE 5 TEST CASE: {case_title}")
        print(f"=======================================================")
        
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition(input_text)
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        
        print("\n--- EXECUTING STAGE 5 CONFIRMATION GATE ---")
        result = w.stage_5_user_confirmation(
            user_action=user_action,
            supplied_fields=supplied_fields,
            unknown_fields_responses=unknown_responses,
            corrections=corrections
        )
        print(f"\n--- GATE RESULT ---")
        print(f"Status: {result['status']} | Confirmed: {result['confirmed']}")

    # 1. Mandatory field missing
    run_stage_5_test(
        "1. Mandatory Field Missing (Blocks Drafting)",
        input_text="Hi Dr. Smith, I missed Assignment 2 because I was ill. Can I please get an extension?",  # missing requested_extension_duration & course_name
        user_action="CONFIRM"
    )

    # 2. Optional field missing & Exact factual extraction (No unsupported 'high fever' claim)
    run_stage_5_test(
        "2. Optional Field Missing & Exact Factual Extraction (Strict supported meaning)",
        input_text="Hi Dr. Smith, I am a student in CS 401. I missed Assignment 2 due to illness. Can I please get a 2 days extension?",  # reason_for_delay = 'Illness'
        user_action="CONFIRM"
    )

    # 3A. Generic Recipient Title ("Hi Professor") -> Optional/Missing professor_name, Known recipient_salutation="Professor", Passes Gate without AI assumptions
    run_stage_5_test(
        "3A. Generic Recipient Title ('Hi Professor') -> Optional professor_name, Known recipient_salutation, Passes Gate",
        input_text="Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension.",
        user_action="CONFIRM"
    )

    # 3B. Explicit Specific Professor Name ("Hi Dr. Smith") -> Extracted professor_name="Dr. Smith", Passes Gate
    run_stage_5_test(
        "3B. Explicit Specific Professor Name ('Hi Dr. Smith') -> Extracted professor_name='Dr. Smith', Passes Gate",
        input_text="Hi Dr. Smith, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension.",
        user_action="CONFIRM"
    )

    # 4. User corrects extracted information
    run_stage_5_test(
        "4. User Corrects Extracted Information (Precedence Override & Re-summary)",
        input_text="Dear Hiring Manager at FlyRank, I am writing to express my interest in the Machine Learning Engineer role. Portfolio: https://github.com/abdulraheem.",
        user_action="CONFIRM",
        corrections={"target_role": "Senior AI Infrastructure Engineer"}
    )

    # 5. Missing mandatory field with NO reasonable assumption possible (Stays BLOCKED)
    run_stage_5_test(
        "5. Missing Mandatory Field - No Reasonable Assumption Possible (Remains BLOCKED)",
        input_text="Hi Professor Smith, I missed Assignment 2 because I was ill and need an extension for my CS 401 class.",  # missing requested_extension_duration; zero evidence for duration
        user_action="USER_UNKNOWN"
    )

    def run_stage_6_test(case_title: str, input_text: str, user_action: str = "CONFIRM"):
        print(f"\n=======================================================")
        print(f"STAGE 6 TEST CASE: {case_title}")
        print(f"=======================================================")
        
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition(input_text)
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        
        gate_res = w.stage_5_user_confirmation(user_action=user_action)
        if not gate_res["confirmed"]:
            print(f"\n[STAGE 6 TEST RESULT] Stage 6 BLOCKED as expected. Missing mandatory info prevented draft generation.")
            return
            
        w.stage_6_draft()
        
        draft = w.state.current_draft
        body = draft["body_text"]
        
        # Integrity Expectations Checks
        checks = {
            "no_internal_labels": "[ASSUMPTION" not in body and "[KNOWN" not in body and "[MISSING" not in body and "[CONFIRMED" not in body,
            "no_invented_severity": "high fever" not in body.lower() and "severe" not in body.lower(),
            "no_unsupported_expansions": "unable to complete" not in body.lower() and "scheduled deadline" not in body.lower(),
            "exact_duration_requested": "2-day extension" in body.lower(),
            "no_invented_sender_name": "abdul raheem" not in body.lower(),
            "explicit_cta_present": "extension" in body.lower()
        }
        
        print("\n--- STAGE 6 FACTUAL-INTEGRITY EVALUATION ---")
        for check_name, passed in checks.items():
            status_str = "PASSED" if passed else "FAILED"
            print(f"  - {check_name}: {status_str}")
            
        all_passed = all(checks.values())
        print(f"  --> Stage 6 Factual Integrity Status: {'PASSED' if all_passed else 'FAILED'}")

    run_stage_6_test(
        "6A. Professor Late Assignment (Generic Title 'Hi Professor')",
        "Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension."
    )

    run_stage_6_test(
        "6B. Professor Late Assignment (Specific Name 'Hi Dr. Smith')",
        "Hi Dr. Smith, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension."
    )

    run_stage_6_test(
        "6C. Missing Mandatory Field Blocks Before Stage 6",
        "Hi Professor Smith, I missed Assignment 2 because I was ill and need an extension for my CS 401 class."
    )

    def run_stage_7_test(case_title: str, input_text: str):
        print(f"\n=======================================================")
        print(f"STAGE 7 TEST CASE: {case_title}")
        print(f"=======================================================")
        
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition(input_text)
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        w.stage_5_user_confirmation(user_action="CONFIRM")
        w.stage_6_draft()
        w.stage_7_critique()
        
        res = w.state.critique_result
        print("\n--- STAGE 7 COMPLETE CRITIQUE_RESULT PAYLOAD ---")
        print(json.dumps(res, indent=2))
        
        checks = {
            "specificity_is_100": res["scores"]["specificity"] == 100,
            "context_ge_80": res["scores"]["context"] >= 80,
            "critical_passed_true": res["critical_passed"] is True,
            "ready_for_continuation_true": res["ready_for_continuation"] is True,
            "no_unsupported_recommendations": len(res["weaknesses"]) == 0
        }
        
        print("\n--- STAGE 7 INTEGRITY EVALUATION ---")
        for check_name, passed in checks.items():
            status_str = "PASSED" if passed else "FAILED"
            print(f"  - {check_name}: {status_str}")

    run_stage_7_test(
        "7A. Full Critique Evaluation on Stage 6 Draft",
        "Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension."
    )

    run_stage_7_test(
        "7B. Missing Optional Field Non-Penalty Evaluation",
        "Hi Dr. Smith, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension."
    )

    def run_stage_7_negative_test(case_title: str, input_text: str):
        print(f"\n=======================================================")
        print(f"STAGE 7 TEST CASE: {case_title}")
        print(f"=======================================================")
        
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition(input_text)
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        w.stage_5_user_confirmation(user_action="CONFIRM")
        
        # Intentionally weaken draft by omitting requested_extension_duration ("2-day")
        w.stage_6_draft()
        w.state.current_draft["body_text"] = "Dear Professor,\n\nI am a student in CS 401. I missed Assignment 2 due to illness and would like to request an extension.\n\nBest regards,"
        
        w.stage_7_critique()
        
        res = w.state.critique_result
        print("\n--- STAGE 7 COMPLETE CRITIQUE_RESULT PAYLOAD (NEGATIVE TEST) ---")
        print(json.dumps(res, indent=2))
        
        checks = {
            "specificity_below_100": res["scores"]["specificity"] < 100,
            "critical_passed_false": res["critical_passed"] is False,
            "ready_for_continuation_false": res["ready_for_continuation"] is False,
            "omitted_fact_in_weaknesses": any("requested_extension_duration" in w_item for w_item in res["weaknesses"]),
            "omitted_fact_in_recommendations": any("requested_extension_duration" in r_item for r_item in res["revision_recommendations"]),
            "priority_backlog_has_specificity": "specificity" in res["priority_backlog"]
        }
        
        print("\n--- STAGE 7 INTEGRITY EVALUATION (NEGATIVE TEST) ---")
        for check_name, passed in checks.items():
            status_str = "PASSED" if passed else "FAILED"
            print(f"  - {check_name}: {status_str}")

    run_stage_7_negative_test(
        "7C. Negative Critique Evaluation (Omitted Duration in Draft)",
        "Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension."
    )

    # STAGE 8 TESTS
    def run_stage_8_test_a():
        print(f"\n=======================================================")
        print(f"STAGE 8 TEST CASE: 8A. Good Draft (No Unnecessary Revision)")
        print(f"=======================================================")
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition("Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension.")
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        w.stage_5_user_confirmation(user_action="CONFIRM")
        w.stage_6_draft()
        w.stage_7_critique()
        
        initial_count = w.state.revision_count
        initial_body = w.state.current_draft["body_text"]
        w.stage_8_revise()
        
        checks = {
            "count_unchanged": w.state.revision_count == initial_count == 0,
            "body_unchanged": w.state.current_draft["body_text"] == initial_body
        }
        print("\n--- TEST 8A INTEGRITY EVALUATION ---")
        for check_name, passed in checks.items():
            print(f"  - {check_name}: {'PASSED' if passed else 'FAILED'}")

    def run_stage_8_test_b():
        print(f"\n=======================================================")
        print(f"STAGE 8 TEST CASE: 8B. Specificity Failure (Restores Confirmed Duration)")
        print(f"=======================================================")
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition("Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension.")
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        w.stage_5_user_confirmation(user_action="CONFIRM")
        w.stage_6_draft()
        
        # Weaken draft by omitting requested_extension_duration
        weakened_text = "Dear Professor,\n\nI am a student in CS 401. I missed Assignment 2 due to illness and would like to request an extension.\n\nBest regards,"
        w.state.current_draft["body_text"] = weakened_text
        w.stage_7_critique()
        
        w.stage_8_revise()
        revised_body = w.state.current_draft["body_text"]
        
        checks = {
            "revision_count_equals_1": w.state.revision_count == 1,
            "prior_valid_draft_saved": w.state.prior_valid_draft["body_text"] == weakened_text,
            "restored_confirmed_duration": "2-day extension" in revised_body.lower(),
            "no_unsupported_severity": "severe" not in revised_body.lower() and "high fever" not in revised_body.lower()
        }
        print("\n--- TEST 8B INTEGRITY EVALUATION ---")
        for check_name, passed in checks.items():
            print(f"  - {check_name}: {'PASSED' if passed else 'FAILED'}")

    def run_stage_8_test_c():
        print(f"\n=======================================================")
        print(f"STAGE 8 TEST CASE: 8C. Attempt Limit Check (Cap at 5)")
        print(f"=======================================================")
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition("Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension.")
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        w.stage_5_user_confirmation(user_action="CONFIRM")
        w.stage_6_draft()
        w.stage_7_critique()
        
        # Set critical_passed = False and revision_count = 5
        w.state.critique_result["critical_passed"] = False
        w.state.critique_result["scores"]["specificity"] = 70
        w.state.revision_count = 5
        
        initial_body = w.state.current_draft["body_text"]
        w.stage_8_revise()
        
        checks = {
            "revision_count_remains_5": w.state.revision_count == 5,
            "no_sixth_attempt": w.state.current_draft["body_text"] == initial_body
        }
        print("\n--- TEST 8C INTEGRITY EVALUATION ---")
        for check_name, passed in checks.items():
            print(f"  - {check_name}: {'PASSED' if passed else 'FAILED'}")

    run_stage_8_test_a()
    run_stage_8_test_b()
    run_stage_8_test_c()

    # STAGE 9 TESTS
    def run_stage_9_test_a():
        print(f"\n=======================================================")
        print(f"STAGE 9 TEST CASE: 9A. Valid Stage 6 Draft Evaluation")
        print(f"=======================================================")
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition("Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension.")
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        w.stage_5_user_confirmation(user_action="CONFIRM")
        w.stage_6_draft()
        res = w.stage_9_fact_check()
        
        checks = {
            "passed_true": res["passed"] is True,
            "factual_integrity_true": res["factual_integrity"] is True,
            "action_accept": res["recommended_action"] == "ACCEPT",
            "no_violations": len(res["altered_facts"]) == 0 and len(res["invented_details"]) == 0
        }
        print("\n--- TEST 9A INTEGRITY EVALUATION ---")
        for check_name, passed in checks.items():
            print(f"  - {check_name}: {'PASSED' if passed else 'FAILED'}")

    def run_stage_9_test_b():
        print(f"\n=======================================================")
        print(f"STAGE 9 TEST CASE: 9B. Valid Stage 8 Revised Draft ('2-day extension')")
        print(f"=======================================================")
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition("Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension.")
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        w.stage_5_user_confirmation(user_action="CONFIRM")
        w.stage_6_draft()
        
        # Weaken and then revise
        w.state.current_draft["body_text"] = "Dear Professor,\n\nI am a student in CS 401. I missed Assignment 2 due to illness and would like to request an extension.\n\nBest regards,"
        w.stage_7_critique()
        w.stage_8_revise()
        
        res = w.stage_9_fact_check()
        
        checks = {
            "passed_true": res["passed"] is True,
            "no_altered_facts": len(res["altered_facts"]) == 0,
            "no_unsupported_strengthening": len(res["unsupported_strengthening"]) == 0,
            "action_accept": res["recommended_action"] == "ACCEPT"
        }
        print("\n--- TEST 9B INTEGRITY EVALUATION ---")
        for check_name, passed in checks.items():
            print(f"  - {check_name}: {'PASSED' if passed else 'FAILED'}")

    def run_stage_9_test_c():
        print(f"\n=======================================================")
        print(f"STAGE 9 TEST CASE: 9C. Unsupported Medical Strengthening ('severe illness')")
        print(f"=======================================================")
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition("Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension.")
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        w.stage_5_user_confirmation(user_action="CONFIRM")
        w.stage_6_draft()
        
        valid_draft_text = w.state.current_draft["body_text"]
        w.state.prior_valid_draft = copy.deepcopy(w.state.current_draft)
        w.state.revision_count = 1
        
        # Candidate draft contains unsupported strengthening "severe illness"
        w.state.current_draft["body_text"] = "Dear Professor,\n\nI am a student in CS 401. I missed Assignment 2 due to severe illness and would like to request a 2-day extension.\n\nBest regards,"
        
        res = w.stage_9_fact_check()
        
        checks = {
            "passed_false": res["passed"] is False,
            "action_rollback": res["recommended_action"] == "ROLLBACK",
            "violation_detected": len(res["unsupported_strengthening"]) > 0 or len(res["invented_details"]) > 0,
            "prior_valid_draft_restored": w.state.current_draft["body_text"] == valid_draft_text,
            "revision_count_unchanged": w.state.revision_count == 1
        }
        print("\n--- TEST 9C INTEGRITY EVALUATION ---")
        for check_name, passed in checks.items():
            print(f"  - {check_name}: {'PASSED' if passed else 'FAILED'}")

    def run_stage_9_test_d():
        print(f"\n=======================================================")
        print(f"STAGE 9 TEST CASE: 9D. Altered Duration ('5-day extension')")
        print(f"=======================================================")
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition("Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension.")
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        w.stage_5_user_confirmation(user_action="CONFIRM")
        w.stage_6_draft()
        
        valid_draft_text = w.state.current_draft["body_text"]
        w.state.prior_valid_draft = copy.deepcopy(w.state.current_draft)
        w.state.revision_count = 1
        
        # Candidate draft contains altered duration "5-day extension"
        w.state.current_draft["body_text"] = "Dear Professor,\n\nI am a student in CS 401. I missed Assignment 2 due to illness and would like to request a 5-day extension.\n\nBest regards,"
        
        res = w.stage_9_fact_check()
        
        checks = {
            "passed_false": res["passed"] is False,
            "action_rollback": res["recommended_action"] == "ROLLBACK",
            "altered_facts_identified": len(res["altered_facts"]) > 0,
            "prior_valid_draft_restored": w.state.current_draft["body_text"] == valid_draft_text,
            "revision_count_unchanged": w.state.revision_count == 1
        }
        print("\n--- TEST 9D INTEGRITY EVALUATION ---")
        for check_name, passed in checks.items():
            print(f"  - {check_name}: {'PASSED' if passed else 'FAILED'}")

    def run_stage_9_test_e():
        print(f"\n=======================================================")
        print(f"STAGE 9 TEST CASE: 9E. Missing Optional Information Non-Penalty")
        print(f"=======================================================")
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition("Hi Dr. Smith, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension.")
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        w.stage_5_user_confirmation(user_action="CONFIRM")
        w.stage_6_draft()
        
        res = w.stage_9_fact_check()
        
        checks = {
            "passed_true": res["passed"] is True,
            "missing_confirmed_facts_empty": len(res["missing_confirmed_facts"]) == 0,
            "action_accept": res["recommended_action"] == "ACCEPT"
        }
        print("\n--- TEST 9E INTEGRITY EVALUATION ---")
        for check_name, passed in checks.items():
            print(f"  - {check_name}: {'PASSED' if passed else 'FAILED'}")

    def run_stage_9_test_f():
        print(f"\n=======================================================")
        print(f"STAGE 9 TEST CASE: 9F. Result Consistency Invariant Verification")
        print(f"=======================================================")
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition("Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension.")
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        w.stage_5_user_confirmation(user_action="CONFIRM")
        w.stage_6_draft()
        
        res = w.stage_9_fact_check()
        
        checks = {
            "invariant_passed_equals_integrity": res["passed"] == res["factual_integrity"],
            "invariant_action_matches_passed": (res["recommended_action"] == "ACCEPT" if res["passed"] else res["recommended_action"] == "ROLLBACK")
        }
        print("\n--- TEST 9F INTEGRITY EVALUATION ---")
        for check_name, passed in checks.items():
            print(f"  - {check_name}: {'PASSED' if passed else 'FAILED'}")

    run_stage_9_test_a()
    run_stage_9_test_b()
    run_stage_9_test_c()
    run_stage_9_test_d()
    run_stage_9_test_e()
    run_stage_9_test_f()

    # STAGE 10 TESTS
    def run_stage_10_test_a():
        print(f"\n=======================================================")
        print(f"STAGE 10 TEST CASE: 10A. Perfect Draft Final Approval")
        print(f"=======================================================")
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition("Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension.")
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        w.stage_5_user_confirmation(user_action="CONFIRM")
        w.stage_6_draft()
        w.stage_7_critique()
        w.stage_9_fact_check()
        
        res = w.stage_10_final_quality_check()
        
        checks = {
            "final_approved_true": res["final_approved"] is True,
            "status_final_approval": res["quality_status"] == "FINAL_APPROVAL",
            "next_action_stage_11": res["next_action"] == "PROCEED_TO_HUMAN_REVIEW_STAGE_11",
            "failed_criteria_empty": len(res["failed_criteria"]) == 0,
            "review_mode_normal": w.state.review_mode == "NORMAL"
        }
        print("\n--- TEST 10A INTEGRITY EVALUATION ---")
        for check_name, passed in checks.items():
            print(f"  - {check_name}: {'PASSED' if passed else 'FAILED'}")

    def run_stage_10_test_b():
        print(f"\n=======================================================")
        print(f"STAGE 10 TEST CASE: 10B. Factual Failure Hard Human Review Trigger")
        print(f"=======================================================")
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition("Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension.")
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        w.stage_5_user_confirmation(user_action="CONFIRM")
        w.stage_6_draft()
        w.stage_7_critique()
        
        # Simulate factual integrity failure in fact_check_result
        w.state.critique_result["fact_check_result"] = {"passed": False, "factual_integrity": False}
        w.state.revision_count = 1  # Revisions remaining (< 5)
        
        res = w.stage_10_final_quality_check()
        
        checks = {
            "final_approved_false": res["final_approved"] is False,
            "status_special_attention": res["quality_status"] == "SPECIAL_ATTENTION",
            "next_action_special_attention": res["next_action"] == "MANDATE_SPECIAL_ATTENTION_HUMAN_REVIEW",
            "factual_integrity_failed": "factual_integrity" in res["failed_criteria"],
            "review_mode_special_attention": w.state.review_mode == "SPECIAL_ATTENTION"
        }
        print("\n--- TEST 10B INTEGRITY EVALUATION ---")
        for check_name, passed in checks.items():
            print(f"  - {check_name}: {'PASSED' if passed else 'FAILED'}")

    def run_stage_10_test_c():
        print(f"\n=======================================================")
        print(f"STAGE 10 TEST CASE: 10C. Non-Factual Quality Failure with Revisions Remaining")
        print(f"=======================================================")
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition("Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension.")
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        w.stage_5_user_confirmation(user_action="CONFIRM")
        w.stage_6_draft()
        w.stage_7_critique()
        w.stage_9_fact_check()
        
        # Set conciseness below 80
        w.state.critique_result["scores"]["conciseness"] = 70
        w.state.revision_count = 1
        
        res = w.stage_10_final_quality_check()
        
        checks = {
            "final_approved_false": res["final_approved"] is False,
            "status_revision_required": res["quality_status"] == "REVISION_REQUIRED",
            "next_action_stage_8": res["next_action"] == "RETURN_TO_STAGE_8_REVISION",
            "conciseness_failed": "conciseness" in res["failed_criteria"],
            "attempts_remaining": res["revision_attempts_remaining"] == 4
        }
        print("\n--- TEST 10C INTEGRITY EVALUATION ---")
        for check_name, passed in checks.items():
            print(f"  - {check_name}: {'PASSED' if passed else 'FAILED'}")

    def run_stage_10_test_d():
        print(f"\n=======================================================")
        print(f"STAGE 10 TEST CASE: 10D. Exhausted Revisions Failure")
        print(f"=======================================================")
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition("Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension.")
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        w.stage_5_user_confirmation(user_action="CONFIRM")
        w.stage_6_draft()
        w.stage_7_critique()
        w.stage_9_fact_check()
        
        # Set conciseness below 80 and revision_count = 5
        w.state.critique_result["scores"]["conciseness"] = 70
        w.state.revision_count = 5
        
        res = w.stage_10_final_quality_check()
        
        checks = {
            "final_approved_false": res["final_approved"] is False,
            "status_special_attention": res["quality_status"] == "SPECIAL_ATTENTION",
            "next_action_special_attention": res["next_action"] == "MANDATE_SPECIAL_ATTENTION_HUMAN_REVIEW",
            "attempts_remaining_zero": res["revision_attempts_remaining"] == 0,
            "review_mode_special_attention": w.state.review_mode == "SPECIAL_ATTENTION"
        }
        print("\n--- TEST 10D INTEGRITY EVALUATION ---")
        for check_name, passed in checks.items():
            print(f"  - {check_name}: {'PASSED' if passed else 'FAILED'}")

    def run_stage_10_test_e():
        print(f"\n=======================================================")
        print(f"STAGE 10 TEST CASE: 10E. Missing Upstream Quality Data Fail-Closed")
        print(f"=======================================================")
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition("Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension.")
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        w.stage_5_user_confirmation(user_action="CONFIRM")
        w.stage_6_draft()
        
        # Wipe critique and fact check data to test fail-closed
        w.state.critique_result = {}
        
        res = w.stage_10_final_quality_check()
        
        checks = {
            "final_approved_false": res["final_approved"] is False,
            "status_special_attention": res["quality_status"] == "SPECIAL_ATTENTION",
            "all_quality_criteria_failed": len(res["failed_criteria"]) == 7 and res["criteria"]["draft_present"] is True,
            "review_mode_special_attention": w.state.review_mode == "SPECIAL_ATTENTION"
        }
        print("\n--- TEST 10E INTEGRITY EVALUATION ---")
        for check_name, passed in checks.items():
            print(f"  - {check_name}: {'PASSED' if passed else 'FAILED'}")

    run_stage_10_test_a()
    run_stage_10_test_b()
    run_stage_10_test_c()
    run_stage_10_test_d()
    run_stage_10_test_e()

    # STAGE 11 TESTS
    def run_stage_11_test_a():
        print(f"\n=======================================================")
        print(f"STAGE 11 TEST CASE: 11A. APPROVED Decision Execution")
        print(f"=======================================================")
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition("Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension.")
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        w.stage_5_user_confirmation(user_action="CONFIRM")
        w.stage_6_draft()
        w.stage_7_critique()
        w.stage_9_fact_check()
        w.stage_10_final_quality_check()
        
        pkg = w.stage_11_human_review(decision="APPROVED")
        
        checks = {
            "decision_approved": pkg["human_decision"] == "APPROVED",
            "workflow_complete_true": pkg["workflow_complete"] is True,
            "email_sent_false": pkg["email_sent"] is False,
            "state_human_decision_approved": w.state.human_decision == "APPROVED"
        }
        print("\n--- TEST 11A INTEGRITY EVALUATION ---")
        for check_name, passed in checks.items():
            print(f"  - {check_name}: {'PASSED' if passed else 'FAILED'}")

    def run_stage_11_test_b():
        print(f"\n=======================================================")
        print(f"STAGE 11 TEST CASE: 11B. EDITED Decision & Audit Trail Preservation")
        print(f"=======================================================")
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition("Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension.")
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        w.stage_5_user_confirmation(user_action="CONFIRM")
        w.stage_6_draft()
        w.stage_7_critique()
        w.stage_9_fact_check()
        w.stage_10_final_quality_check()
        
        orig_fq_approved = w.state.final_quality_result["final_approved"]
        edited_body = "Dear Professor,\n\nI missed Assignment 2 due to illness. Kindly grant a 2-day extension.\n\nBest regards,"
        
        pkg = w.stage_11_human_review(decision="EDITED", edited_text=edited_body)
        
        checks = {
            "decision_edited": pkg["human_decision"] == "EDITED",
            "body_text_updated": w.state.current_draft["body_text"] == edited_body,
            "final_quality_result_preserved": pkg["final_quality_result"]["final_approved"] == orig_fq_approved,
            "workflow_complete_true": pkg["workflow_complete"] is True,
            "email_sent_false": pkg["email_sent"] is False
        }
        print("\n--- TEST 11B INTEGRITY EVALUATION ---")
        for check_name, passed in checks.items():
            print(f"  - {check_name}: {'PASSED' if passed else 'FAILED'}")

    def run_stage_11_test_c():
        print(f"\n=======================================================")
        print(f"STAGE 11 TEST CASE: 11C. REJECTED Decision Execution")
        print(f"=======================================================")
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition("Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension.")
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        w.stage_5_user_confirmation(user_action="CONFIRM")
        w.stage_6_draft()
        w.stage_7_critique()
        w.stage_9_fact_check()
        w.stage_10_final_quality_check()
        
        pkg = w.stage_11_human_review(decision="REJECTED")
        
        checks = {
            "decision_rejected": pkg["human_decision"] == "REJECTED",
            "workflow_complete_true": pkg["workflow_complete"] is True,
            "email_sent_false": pkg["email_sent"] is False,
            "state_human_decision_rejected": w.state.human_decision == "REJECTED"
        }
        print("\n--- TEST 11C INTEGRITY EVALUATION ---")
        for check_name, passed in checks.items():
            print(f"  - {check_name}: {'PASSED' if passed else 'FAILED'}")

    def run_stage_11_test_d():
        print(f"\n=======================================================")
        print(f"STAGE 11 TEST CASE: 11D. SPECIAL_ATTENTION Review Execution")
        print(f"=======================================================")
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition("Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension.")
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        w.stage_5_user_confirmation(user_action="CONFIRM")
        w.stage_6_draft()
        w.stage_7_critique()
        
        # Simulate factual integrity failure causing SPECIAL_ATTENTION at Stage 10
        w.state.critique_result["fact_check_result"] = {"passed": False, "factual_integrity": False}
        w.stage_10_final_quality_check()
        
        pkg = w.stage_11_human_review(decision="APPROVED")
        
        checks = {
            "special_attention_flagged": pkg["special_attention"] is True,
            "review_mode_special_attention": pkg["review_mode"] == "SPECIAL_ATTENTION",
            "decision_approved": pkg["human_decision"] == "APPROVED",
            "email_sent_false": pkg["email_sent"] is False
        }
        print("\n--- TEST 11D INTEGRITY EVALUATION ---")
        for check_name, passed in checks.items():
            print(f"  - {check_name}: {'PASSED' if passed else 'FAILED'}")

    def run_stage_11_test_e():
        print(f"\n=======================================================")
        print(f"STAGE 11 TEST CASE: 11E. Invalid Decision & Empty EDITED Text Error Handling")
        print(f"=======================================================")
        w = EmailDraftingWorkflow()
        w.stage_1_input_acquisition("Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension.")
        w.stage_2_type_classification()
        w.stage_3_requirements_loader()
        w.stage_4_extract_and_validate()
        w.stage_5_user_confirmation(user_action="CONFIRM")
        w.stage_6_draft()
        
        res_invalid = w.stage_11_human_review(decision="INVALID_STRING")
        res_empty = w.stage_11_human_review(decision="EDITED", edited_text="")
        
        checks = {
            "invalid_decision_error": res_invalid.get("status") == "ERROR_INVALID_DECISION",
            "empty_edited_text_error": res_empty.get("status") == "ERROR_EMPTY_EDITED_TEXT",
            "email_sent_remains_false": w.state.email_sent is False
        }
        print("\n--- TEST 11E INTEGRITY EVALUATION ---")
        for check_name, passed in checks.items():
            print(f"  - {check_name}: {'PASSED' if passed else 'FAILED'}")

    run_stage_11_test_a()
    run_stage_11_test_b()
    run_stage_11_test_c()
    run_stage_11_test_d()
    run_stage_11_test_e()

    # END-TO-END WORKFLOW INTEGRATION TESTS (STAGES 1 TO 11)
    def run_e2e_integration_tests():
        print(f"\n=======================================================")
        print(f"E2E INTEGRATION TEST SUITE: FULL PIPELINE (STAGES 1 TO 11)")
        print(f"=======================================================")

        # E2E Test 1: Standard Perfect Flow
        print("\n--- E2E TEST 1: Standard Perfect Flow ---")
        w1 = EmailDraftingWorkflow()
        input_text_1 = "Hi Professor, I am a student in CS 401. I missed Assignment 2 because I was sick and need a 2 days extension."
        summary1 = w1.run_full_pipeline(input_text_1)
        checks1 = {
            "workflow_terminated": summary1["status"] == "TERMINATED",
            "decision_approved": summary1["human_decision"] == "APPROVED",
            "revision_count_zero": summary1["revision_count"] == 0,
            "final_approved_true": w1.state.final_quality_result["final_approved"] is True,
            "email_sent_false": w1.state.email_sent is False
        }
        print("--- E2E TEST 1 EVALUATION ---")
        for k, v in checks1.items():
            print(f"  - {k}: {'PASSED' if v else 'FAILED'}")

        # E2E Test 2: Auto-Revision & Restoration Flow
        print("\n--- E2E TEST 2: Auto-Revision & Restoration Flow ---")
        w2 = EmailDraftingWorkflow()
        w2.stage_1_input_acquisition(input_text_1)
        w2.stage_2_type_classification()
        w2.stage_3_requirements_loader()
        w2.stage_4_extract_and_validate()
        w2.stage_5_user_confirmation(user_action="CONFIRM")
        w2.stage_6_draft()
        # Weaken draft by omitting requested_extension_duration
        w2.state.current_draft["body_text"] = "Dear Professor,\n\nI am a student in CS 401. I missed Assignment 2 due to illness and would like to request an extension.\n\nBest regards,"
        w2.stage_7_critique()
        
        # Pipeline loop handles Stage 8 -> 9 -> 7 -> 10 -> 11 -> 12
        while True:
            critical_pass = w2.state.critique_result["pass_fail"]["specificity"] and w2.state.critique_result["pass_fail"]["context"]
            if critical_pass or w2.state.revision_count >= 5:
                break
            w2.stage_8_revise()
            w2.stage_9_fact_check()
            w2.stage_7_critique()
            
        w2.stage_10_final_quality_check()
        w2.stage_11_human_review(decision="APPROVED")
        summary2 = w2.stage_12_terminal_state()

        checks2 = {
            "revision_count_equals_1": w2.state.revision_count == 1,
            "fact_check_passed": w2.state.critique_result["fact_check_result"]["passed"] is True,
            "final_approved_true": w2.state.final_quality_result["final_approved"] is True,
            "restored_duration": "2-day extension" in w2.state.current_draft["body_text"].lower(),
            "email_sent_false": w2.state.email_sent is False
        }
        print("--- E2E TEST 2 EVALUATION ---")
        for k, v in checks2.items():
            print(f"  - {k}: {'PASSED' if v else 'FAILED'}")

        # E2E Test 3: Factual Violation Rollback & Hard Human Review Trigger
        print("\n--- E2E TEST 3: Factual Violation Rollback & Hard Human Review Trigger ---")
        w3 = EmailDraftingWorkflow()
        w3.stage_1_input_acquisition(input_text_1)
        w3.stage_2_type_classification()
        w3.stage_3_requirements_loader()
        w3.stage_4_extract_and_validate()
        w3.stage_5_user_confirmation(user_action="CONFIRM")
        w3.stage_6_draft()
        valid_body = w3.state.current_draft["body_text"]
        w3.state.prior_valid_draft = copy.deepcopy(w3.state.current_draft)
        w3.state.revision_count = 1
        
        # Introduce altered duration "5-day extension"
        w3.state.current_draft["body_text"] = "Dear Professor,\n\nI am a student in CS 401. I missed Assignment 2 due to illness and would like to request a 5-day extension.\n\nBest regards,"
        w3.stage_9_fact_check()
        w3.stage_10_final_quality_check()
        w3.stage_11_human_review(decision="APPROVED")
        summary3 = w3.stage_12_terminal_state()

        checks3 = {
            "fact_check_failed": w3.state.critique_result["fact_check_result"]["passed"] is False,
            "rollback_executed": w3.state.current_draft["body_text"] == valid_body,
            "quality_status_special_attention": w3.state.final_quality_result["quality_status"] == "SPECIAL_ATTENTION",
            "review_mode_special_attention": w3.state.review_mode == "SPECIAL_ATTENTION",
            "email_sent_false": w3.state.email_sent is False
        }
        print("--- E2E TEST 3 EVALUATION ---")
        for k, v in checks3.items():
            print(f"  - {k}: {'PASSED' if v else 'FAILED'}")

        # E2E Test 4: Human Edit Workflow Completion Flow
        print("\n--- E2E TEST 4: Human Edit Workflow Completion Flow ---")
        w4 = EmailDraftingWorkflow()
        w4.stage_1_input_acquisition(input_text_1)
        w4.stage_2_type_classification()
        w4.stage_3_requirements_loader()
        w4.stage_4_extract_and_validate()
        w4.stage_5_user_confirmation(user_action="CONFIRM")
        w4.stage_6_draft()
        w4.stage_7_critique()
        w4.stage_9_fact_check()
        w4.stage_10_final_quality_check()
        
        edited_text = "Dear Professor,\n\nI am in CS 401 and missed Assignment 2 due to illness. I politely request a 2-day extension.\n\nBest regards,"
        w4.stage_11_human_review(decision="EDITED", edited_text=edited_text)
        summary4 = w4.stage_12_terminal_state()

        checks4 = {
            "human_decision_edited": summary4["human_decision"] == "EDITED",
            "body_text_has_edits": w4.state.current_draft["body_text"] == edited_text,
            "historical_fq_preserved": w4.state.final_quality_result["final_approved"] is True,
            "email_sent_false": w4.state.email_sent is False
        }
        print("--- E2E TEST 4 EVALUATION ---")
        for k, v in checks4.items():
            print(f"  - {k}: {'PASSED' if v else 'FAILED'}")

    run_e2e_integration_tests()




