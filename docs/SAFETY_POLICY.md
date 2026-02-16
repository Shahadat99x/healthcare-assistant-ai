# Safety Policy & Mechanisms (Phase 2)

This document outlines the deterministic safety rules implemented in the Healthcare Assistant.

## 1. Classification Levels

The system classifies every user message into one of four urgency levels:

- **Emergency (`emergency`)**: Life-threatening conditions (Safety Service) or severe symptoms (Triage).
- **Urgent (`urgent`)**: Serious conditions requiring timely care (e.g. High fever > 39C, breathing difficulty).
- **Routine (`routine`)**: Long-standing (>7 days) or non-worsening symptoms.
- **Self Care (`self_care`)**: Mild, short-term issues (e.g. mild cold).
- **Unknown (`unknown`)**: Vague symptoms requiring clarification.

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

- **Safety Service** (`apps/api/services/safety_service.py`):
  - Primary Gate for Red Flags (Emergency Lock).
  - Regex-based refusal for out-of-scope topics.
- **Triage Service** (`apps/api/services/triage_service.py`) (Phase 3):
  - Secondary Risk Stratification.
  - Parses symptoms, severity, and duration.
  - Assigns `urgent`, `routine`, `self_care`, or `unknown`.
- **Grounding Enforcement**:
  - If RAG retrieves no relevant guidelines, the system refuses to provide specific medical advice.
