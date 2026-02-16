import requests
import json
import time
import os
from datetime import datetime

API_URL = "http://127.0.0.1:8000/chat"
EVAL_FILE = "eval/triage_prompts.jsonl"
OUTPUT_DIR = f"eval/rag_health/{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def ensure_dir(d):
    global OUTPUT_DIR
    # Fix paths for Windows
    d = d.replace("/", os.sep)
    if not os.path.exists(d):
        os.makedirs(d)

def run_health_check():
    ensure_dir(OUTPUT_DIR)
    results = []
    
    print(f"--- Starting RAG Health Check (Phase 4) ---")
    print(f"Reading prompts from: {EVAL_FILE}")
    
    with open(EVAL_FILE, "r") as f:
        prompts = [json.loads(line) for line in f if line.strip()]

    total = 0
    medical_count = 0
    grounded_count = 0
    empty_rag_count = 0
    org_distribution = {}

    for p in prompts:
        msg = p["prompt"]
        category = p["category"]
        print(f"\nProcessing: '{msg}' [{category}]")
        
        # Use unique session to avoid lock state pollution
        session_id = f"health_check_{int(time.time())}_{total}"
        
        try:
            res = requests.post(
                API_URL, 
                json={"message": msg, "mode": "rag", "session_id": session_id}
            ).json()
            
            # Metrics from Response Meta
            total += 1
            intent = res.get("intent", "unknown")
            response_kind = res.get("response_kind", "unknown")
            urgency = res.get("urgency", "unknown")
            lock_state = res.get("lock_state", "none")
            citations = res.get("citations", [])
            
            outcome = {
                "prompt": msg,
                "category": category,
                "intent": intent,
                "response_kind": response_kind,
                "urgency": urgency,
                "lock_state": lock_state,
                "citation_count": len(citations),
                "orgs": list(set([c.get("org", "Unknown") for c in citations]))
            }
            results.append(outcome)

            # Logic for "Medical & Grounded"
            # We only count it as "medical" if intent is medical_symptoms OR urgency is not self_care/unknown
            is_medical_intent = (intent == "medical_symptoms")
            
            if is_medical_intent:
                medical_count += 1
                if citations:
                    grounded_count += 1
                    for c in citations:
                        org = c.get("org", "Unknown")
                        org_distribution[org] = org_distribution.get(org, 0) + 1
                else:
                    # If medical but no citations -> Empty RAG
                    # BUT if urgency is 'emergency' (lockout), it's NOT a RAG failure, it's a safety bypass.
                    # RAG failure is only if we tried to get help but got no docs.
                    if urgency != "emergency" and lock_state != "active":
                         empty_rag_count += 1
            
            print(f" -> Intent: {intent}, Urgency: {urgency}, Citations: {len(citations)}")
            
        except Exception as e:
            print(f"Error: {e}")

    # Metrics Calc
    coverage = (grounded_count / medical_count * 100) if medical_count else 0
    empty_rate = (empty_rag_count / medical_count * 100) if medical_count else 0 # Rough proxy
    
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "total_prompts": total,
        "medical_prompts": medical_count,
        "grounded_responses": grounded_count,
        "citation_coverage_rate": round(coverage, 2),
        "empty_retrieval_count": empty_rag_count,
        "org_distribution": org_distribution
    }

    # Save
    metrics_path = f"{OUTPUT_DIR}/metrics.json"
    details_path = f"{OUTPUT_DIR}/details.jsonl"
    
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
        
    with open(details_path, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    print(f"\n--- Health Check Complete ---")
    print(f"Metric File: {metrics_path}")
    print(f"Coverage: {coverage}%")
    print(f"Top Orgs: {org_distribution}")

if __name__ == "__main__":
    run_health_check()
