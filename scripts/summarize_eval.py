import json
import os
import glob
from collections import Counter

def summarize_eval(results_dir="eval/results"):
    print(f"Summarizing Evaluation Results from: {results_dir}")
    
    files = glob.glob(os.path.join(results_dir, "*.jsonl"))
    if not files:
        print("No result files found.")
        return

    urgency_counts = Counter()
    citations_used_count = 0
    total_medical = 0
    total_unknown = 0
    total_entries = 0
    
    for file_path in files:
        print(f"Processing {file_path}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip(): continue
                    total_entries += 1
                    try:
                        data = json.loads(line)
                        intent = data.get("intent", "unknown")
                        urgency = data.get("urgency", "unknown")
                        citations = data.get("citations", [])
                        
                        urgency_counts[urgency] += 1
                        
                        if intent == "medical_symptoms":
                            total_medical += 1
                            if citations:
                                citations_used_count += 1
                            if urgency == "unknown":
                                total_unknown += 1
                                
                    except json.JSONDecodeError as e:
                        print(f"JSON Error: {e}")
        except Exception as e:
            print(f"File Error: {e}")

    if total_entries == 0:
        print("No entries found.")
        return

    print("\n--- Triage Summary ---")
    print(f"Total Interactions: {total_entries}")
    print("\nUrgency Distribution:")
    for k, v in urgency_counts.items():
        print(f"  {k}: {v} ({v/total_entries*100:.1f}%)")
        
    print(f"\nMedical Queries: {total_medical}")
    if total_medical > 0:
        print(f"Citations Used: {citations_used_count} ({citations_used_count/total_medical*100:.1f}% of medical queries)")
    print(f"Unknown Urgency (Clarification needed): {total_unknown}")

if __name__ == "__main__":
    summarize_eval()
