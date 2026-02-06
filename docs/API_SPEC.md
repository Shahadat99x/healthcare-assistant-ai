# API_SPEC — HTTP Endpoints (MVP)

## 1) Base rules
- JSON request/response
- No PII storage required for MVP
- All responses include safety metadata

## 2) Endpoints

### POST /chat
**Request**
```json
{
  "session_id": "string",
  "message": "string",
  "mode": "baseline|rag|rag_safety"
}


{
  "assistant_message": "string",
  "urgency": "self_care|gp|urgent|emergency",
  "safety_flags": ["red_flag_detected", "refusal_applied"],
  "citations": [
    {
      "id": "doc_001#chunk_03",
      "title": "Source title",
      "snippet": "Short excerpt...",
      "source_type": "medical_guideline|local_policy",
      "last_updated": "YYYY-MM-DD"
    }
  ],
  "recommendations": [
    {
      "type": "facility",
      "name": "Clinic/Hospital name",
      "specialty": "ENT",
      "address": "string",
      "phone": "string",
      "hours": "string",
      "booking_url": "string"
    }
  ]
}


{
  "error": {
    "code": "MODEL_UNAVAILABLE|INDEX_MISSING|VALIDATION_ERROR",
    "message": "string"
  }
}
