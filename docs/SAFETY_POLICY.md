# Safety Policy & Mechanisms (Phase 2)

This document outlines the deterministic safety rules implemented in the Healthcare Assistant.

## 1. Classification Levels

The system classifies every user message into one of four urgency levels:

- **Emergency (`emergency`)**: Life-threatening conditions requiring immediate action.
- **Urgent (`urgent`)**: Serious conditions requiring timely medical attention.
- **GP (`gp`)**: Non-urgent issues suitable for a General Practitioner.
- **Self Care (`self_care`)**: Minor issues manageble at home (default).

## 2. Deterministic Rules (Regex-Based)

### A. Emergency Escalation (Red Flags)

**Action**: `escalate` (Refuse to chat, order immediate care).
**Keywords**:

- `chest pain`
- `difficulty breathing`
- `stroke` (face droop, slurred speech)
- `severe bleeding`
- `anaphylaxis` (throat swelling)
- `suicidal`

**Response**:

> "EMERGENCY ALERT: ... Call 112 or go to the nearest emergency room."

### B. Medical Scope Refusal

**Action**: `refuse` (Refuse to provide specific advice).
**Keywords**:

- `dosage`, `dose`, `mg`
- `prescribe`, `prescription`
- `antibiotic`
- `confirm diagnosis`

**Response**:

> "I cannot provide specific medical diagnoses, prescriptions, or dosage instructions..."

### C. General Disclaimer

**Action**: `allow` (with disclaimer).
Appended to all other responses:

> "I’m not a doctor. If symptoms worsen or you have serious concerns, seek medical care."

## 3. Implementation Details

- **Service**: `apps/api/services/safety_service.py`
- **Method**: `evaluate_user_message(text)` matches text against pre-defined regex lists.
- **Priority**: Emergency > Refusal > Allow.
