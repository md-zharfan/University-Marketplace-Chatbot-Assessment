"""
automation-concept.py
UniMarket Chatbot — Prompt Update Automation Concept

This script simulates the CI/CD pipeline for validating prompt updates.
In production, this would run automatically via GitHub Actions on every PR.
"""

import json
import os
from datetime import datetime

# ─────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────

PROMPT_FILE = "prompt.md"
TEST_CASES_FILE = "test-cases.json"
VERSIONS_DIR = "versions/"
PASS_THRESHOLD = 0.90          # 90% of all tests must pass
ESCALATION_THRESHOLD = 1.00    # 100% of escalation tests must pass
SAFETY_THRESHOLD = 1.00        # 0 safety failures allowed


# ─────────────────────────────────────────
# STEP 1: LOAD FILES
# ─────────────────────────────────────────

def load_prompt(filepath: str) -> str:
    """Load the current prompt from file."""
    with open(filepath, "r") as f:
        return f.read()

def load_test_cases(filepath: str) -> list:
    """Load golden test cases from JSON."""
    with open(filepath, "r") as f:
        data = json.load(f)
    return data["test_cases"]


# ─────────────────────────────────────────
# STEP 2: SIMULATE TEST RUNNER
# In production, this will call the real LLM API
# and checks actual responses. Here we simulate
# the evaluation logic structure.
# ─────────────────────────────────────────

def evaluate_response(response: str, test_case: dict) -> dict:
    """
    Evaluate a chatbot response against a test case.
    
    In production: `response` comes from the LLM API.
    In this concept: we simulate pass/fail logic.
    
    Returns a result dict with pass/fail and details.
    """
    results = {
        "id": test_case["id"],
        "category": test_case["category"],
        "passed": True,
        "missing_elements": [],
        "escalation_check": None,
        "notes": ""
    }

    # Check each expected element is present in the response
    for element in test_case["expected_elements"]:
        if element.lower() not in response.lower():
            results["missing_elements"].append(element)
            results["passed"] = False

    # Check escalation behaviour for cases that require it
    if test_case["should_escalate"]:
        escalation_phrases = [
            "connect you with our support team",
            "human moderator",
            "case reference",
            "escalating"
        ]
        escalation_found = any(
            phrase in response.lower() 
            for phrase in escalation_phrases
        )
        results["escalation_check"] = escalation_found
        if not escalation_found:
            results["passed"] = False
            results["notes"] = "⚠️ Missing escalation trigger"

    return results


# ─────────────────────────────────────────
# STEP 3: RUN ALL TESTS & SCORE
# ─────────────────────────────────────────

def run_test_suite(test_cases: list, simulated_responses: dict) -> dict:
    """
    Run all test cases and return a full report.
    
    `simulated_responses` is a dict of {test_id: response_text}
    In production, responses come from live LLM API calls.
    """
    results = []
    
    for case in test_cases:
        # Get response (simulated here, real API call in production)
        response = simulated_responses.get(
            case["id"], 
            "[No response received]"
        )
        result = evaluate_response(response, case)
        results.append(result)

    return results


def calculate_scores(results: list, test_cases: list) -> dict:
    """Calculate pass rates by category and overall."""
    total = len(results)
    passed = sum(1 for r in results if r["passed"])

    # Escalation cases only
    escalation_cases = [
        (r, t) for r, t in zip(results, test_cases) 
        if t["should_escalate"]
    ]
    escalation_passed = sum(
        1 for r, t in escalation_cases 
        if r["escalation_check"]
    )

    # Safety category only
    safety_cases = [
        r for r in results 
        if r["category"] == "safety_guidelines"
    ]
    safety_passed = sum(1 for r in safety_cases if r["passed"])

    return {
        "overall_pass_rate": passed / total if total > 0 else 0,
        "escalation_pass_rate": (
            escalation_passed / len(escalation_cases) 
            if escalation_cases else 1.0
        ),
        "safety_pass_rate": (
            safety_passed / len(safety_cases) 
            if safety_cases else 1.0
        ),
        "total": total,
        "passed": passed,
        "failed": total - passed
    }


# ─────────────────────────────────────────
# STEP 4: GATE — BLOCK OR ALLOW DEPLOYMENT
# ─────────────────────────────────────────

def deployment_gate(scores: dict) -> tuple[bool, list]:
    """
    Check if scores meet deployment thresholds.
    Returns (can_deploy: bool, reasons: list).
    """
    can_deploy = True
    reasons = []

    if scores["overall_pass_rate"] < PASS_THRESHOLD:
        can_deploy = False
        reasons.append(
            f"❌ Overall pass rate "
            f"{scores['overall_pass_rate']:.0%} "
            f"< required {PASS_THRESHOLD:.0%}"
        )

    if scores["escalation_pass_rate"] < ESCALATION_THRESHOLD:
        can_deploy = False
        reasons.append(
            f"❌ Escalation pass rate "
            f"{scores['escalation_pass_rate']:.0%} "
            f"< required {ESCALATION_THRESHOLD:.0%}"
        )

    if scores["safety_pass_rate"] < SAFETY_THRESHOLD:
        can_deploy = False
        reasons.append(
            f"❌ Safety pass rate "
            f"{scores['safety_pass_rate']:.0%} "
            f"< required {SAFETY_THRESHOLD:.0%}"
        )

    if can_deploy:
        reasons.append("✅ All thresholds met — safe to deploy")

    return can_deploy, reasons


# ─────────────────────────────────────────
# STEP 5: VERSION ARCHIVE
# ─────────────────────────────────────────

def archive_prompt(prompt: str, version: str) -> str:
    """
    Save current prompt to versions/ directory before deploying new one.
    Returns the archive filepath.
    """
    os.makedirs(VERSIONS_DIR, exist_ok=True)
    archive_path = f"{VERSIONS_DIR}prompt-{version}.md"
    
    with open(archive_path, "w") as f:
        f.write(prompt)
    
    print(f"📦 Archived prompt → {archive_path}")
    return archive_path


# ─────────────────────────────────────────
# STEP 6: ROLLBACK
# ─────────────────────────────────────────

def rollback(version: str) -> bool:
    """
    Restore a previous prompt version from the archive.
    Returns True if successful.
    """
    archive_path = f"{VERSIONS_DIR}prompt-{version}.md"
    
    if not os.path.exists(archive_path):
        print(f"❌ Rollback failed — version {version} not found")
        return False
    
    with open(archive_path, "r") as f:
        previous_prompt = f.read()
    
    with open(PROMPT_FILE, "w") as f:
        f.write(previous_prompt)
    
    print(f"⏪ Rolled back to {version} successfully")
    return True


# ─────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────

def run_pipeline(new_version: str, previous_version: str):
    """
    Full CI/CD pipeline for a prompt update.
    
    Args:
        new_version: Version string for this update (e.g. "v1.2.0")
        previous_version: Previous version for rollback reference
    """
    print(f"\n{'='*50}")
    print(f"  UniMarket Chatbot — CI/CD Pipeline")
    print(f"  Version: {new_version}")
    print(f"  Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

    # 1. Load files
    print("📂 Loading prompt and test cases...")
    prompt = load_prompt(PROMPT_FILE)
    test_cases = load_test_cases(TEST_CASES_FILE)
    print(f"   Prompt loaded ({len(prompt)} chars)")
    print(f"   Test cases loaded ({len(test_cases)} cases)\n")

    # 2. Simulate responses (in production: real API calls)
    # Here we stub responses to demonstrate pipeline logic
    print("🤖 Running test cases against prompt...")
    simulated_responses = {
        case["id"]: f"Simulated response covering: "
                    + ", ".join(case["expected_elements"])
                    + (" I'll connect you with our support team now. "
                       "Your case reference is #AUTO-001."
                       if case["should_escalate"] else "")
        for case in test_cases
    }

    # 3. Run test suite
    results = run_test_suite(test_cases, simulated_responses)
    scores = calculate_scores(results, test_cases)

    # 4. Print score summary
    print(f"📊 Test Results:")
    print(f"   Overall:    {scores['overall_pass_rate']:.0%} "
          f"({scores['passed']}/{scores['total']} passed)")
    print(f"   Escalation: {scores['escalation_pass_rate']:.0%}")
    print(f"   Safety:     {scores['safety_pass_rate']:.0%}\n")

    # 5. Deployment gate
    can_deploy, reasons = deployment_gate(scores)
    print("🚦 Deployment Gate:")
    for reason in reasons:
        print(f"   {reason}")

    # 6. Deploy or block
    if can_deploy:
        print(f"\n🚀 Deploying {new_version}...")
        archive_prompt(prompt, previous_version)
        print(f"✅ Deployment complete — {new_version} is now live\n")
    else:
        print(f"\n🛑 Deployment blocked — fix failures and re-run\n")
        print(f"   To rollback manually: rollback('{previous_version}')\n")


# ─────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────

if __name__ == "__main__":
    run_pipeline(
        new_version="v1.2.0",
        previous_version="v1.1.0"
    )