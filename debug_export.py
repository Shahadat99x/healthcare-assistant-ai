import requests
import json
import time

def debug():
    session_id = f"debug_export_{int(time.time())}"
    url = "http://127.0.0.1:8000/chat"
    
    # 1. Send Chitchat
    print("Sending Chitchat...")
    requests.post(url, json={"message": "Hello", "session_id": session_id})
    
    # 2. Send Medical
    print("Sending Medical...")
    requests.post(url, json={"message": "I have a fever", "mode": "rag", "session_id": session_id})
    
    # 3. Export
    print("Exporting...")
    export_url = "http://127.0.0.1:8000/export/chat"
    res = requests.post(export_url, json={"session_id": session_id})
    
    if res.status_code == 200:
        print("Export Success!")
        print(json.dumps(res.json(), indent=2))
    else:
        print(f"Export Failed: {res.status_code}")
        print(res.text)

if __name__ == "__main__":
    debug()
