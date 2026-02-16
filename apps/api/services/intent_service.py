import re
from typing import List, Literal

class IntentService:
    def __init__(self):
        # 1. Chitchat Patterns (Greeting, Thanks, Smalltalk)
        self.chitchat_patterns = [
            r"^(hi|hello|hey|greetings|good morning|good afternoon|good evening)\b",
            r"^(thanks|thank you|thx)\b",
            r"^how are you",
            r"^nice to meet you",
            r"^just checking in"
        ]
        
        # 2. Meta Patterns (About the bot)
        self.meta_patterns = [
            r"what can you do", r"how do you work", r"are you a doctor", 
            r"who created you", r"what is your purpose", r"who are you",
            r"\bsources\b", r"\bprivacy\b", r"\bdata\b"
        ]

        # 3. Logistics Patterns (Emergency numbers, locations) - Basic for Phase 1
        self.logistics_patterns = [
            r"\bcall 112\b", r"\bemergency number\b",
            r"\bhospital\b", r"\bclinic\b", r"\bpharmacy\b", r"\bdoctor near me\b",
            r"\baddress\b", r"\blocation\b"
        ]

        # 4. Symptom Keywords (Overrides chitchat if present)
        # If any of these are found, it's likely medical context even if it starts with "hi"
        self.symptom_keywords = [
            "fever", "cough", "pain", "headache", "vomit", "diarrhea", 
            "chest pain", "breath", "stroke", "bleed", "faint", "seizure", 
            "rash", "swollen", "dizzy", "nause", "ache", "hurt", "injury",
            "sick", "ill", "temperature", "burn", "cut", "wound"
        ]

    def _matches_any(self, text: str, patterns: List[str]) -> bool:
        text_lower = text.lower().strip()
        for pattern in patterns:
            if re.search(pattern, text_lower):
                return True
        return False
        
    def _contains_symptoms(self, text: str) -> bool:
        text_lower = text.lower()
        for keyword in self.symptom_keywords:
            if keyword in text_lower:
                return True
        return False

    def classify_intent(self, text: str) -> Literal["chitchat", "meta", "logistics", "medical_symptoms"]:
        """
        Classifies the user intent based on rule-based matching.
        Order matters: Medical symptoms override chitchat (e.g. "Hi I have fever").
        """
        # 1. Check for medical symptoms first (Safety priority)
        if self._contains_symptoms(text):
            return "medical_symptoms"

        # 2. Logistics
        if self._matches_any(text, self.logistics_patterns):
            return "logistics"

        # 3. Meta
        if self._matches_any(text, self.meta_patterns):
            return "meta"

        # 4. Chitchat
        if self._matches_any(text, self.chitchat_patterns):
            return "chitchat"

        # Default fallback
        return "medical_symptoms"

intent_service = IntentService()
