import re
from pydantic import BaseModel
from typing import List, Literal, Optional

class SafetyResult(BaseModel):
    urgency: Literal["self_care", "gp", "urgent", "emergency"]
    flags: List[str]
    action: Literal["allow", "refuse", "escalate"]
    message_override: Optional[str] = None

class SafetyService:
    def __init__(self):
        # B) Emergency Keywords
        self.emergency_patterns = [
            r"shortness of breath",
            r"difficulty breathing",
            r"can't breathe",
            r"severe breathing",
            r"chest pain",
            r"tightness in chest",
            r"face droop",
            r"slurred speech",
            r"one[- ]sided weakness",
            r"stroke",
            r"uncontrolled bleeding",
            r"severe bleeding",
            r"throat swelling",
            r"swollen tongue",
            r"anaphylaxis",
            r"severe allergic reaction",
            r"seizure",
            r"fainted",
            r"passed out",
            r"suicidal",
            r"kill myself",
            r"self harm"
        ]
        
        # C) Refusal Keywords
        self.refusal_patterns = [
            r"\bdosage\b",
            r"\bdose\b",
            r"\bmg\b",
            r"how many",
            r"how often",
            r"times a day",
            r"\bprescribe\b",
            r"\bantibiotic\b",
            r"\bamoxicillin\b",
            r"\bazithromycin\b",
            r"\bibuprofen dose\b",
            r"do i have",
            r"is it definitely",
            r"confirm diagnosis"
        ]

    def _matches_any(self, text: str, patterns: List[str]) -> bool:
        """Helper to strict regex match case-insensitive."""
        text_lower = text.lower()
        for pattern in patterns:
            if re.search(pattern, text_lower):
                return True
        return False

    def evaluate_user_message(self, text: str) -> SafetyResult:
        # 1. Emergency Escalation
        if self._matches_any(text, self.emergency_patterns):
            msg = (
                "EMERGENCY ALERT: Based on your symptoms, you may be experiencing a life-threatening medical emergency. "
                "Call 112 (or your local emergency number) immediately or go to the nearest emergency room. "
                "Do not delay care."
            )
            return SafetyResult(
                urgency="emergency",
                flags=["red_flag_detected"],
                action="escalate",
                message_override=msg
            )
            
        # 2. Refusal (Medical Advice/Prescription)
        if self._matches_any(text, self.refusal_patterns):
            msg = (
                "I cannot provide specific medical diagnoses, prescriptions, or dosage instructions. "
                "Please consult a doctor or pharmacist for medication advice. "
                "If you are feeling unwell, monitor your symptoms and seek professional care."
            )
            return SafetyResult(
                urgency="self_care",
                flags=["refusal_applied"],
                action="refuse",
                message_override=msg
            )

        # 3. Allow
        return SafetyResult(
            urgency="self_care", # Default
            flags=[],
            action="allow",
            message_override=None
        )

safety_service = SafetyService()
