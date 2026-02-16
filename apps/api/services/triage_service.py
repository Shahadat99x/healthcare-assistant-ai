import re
from typing import Dict, Any

class TriageService:
    def __init__(self):
        # Symptom Keywords mapping
        self.symptoms_map = {
            "fever": ["fever", "temperature", "febrile", "hot"],
            "cough": ["cough", "coughing"],
            "breathing": ["breath", "shortness", "dyspnea", "air"],
            "pain": ["pain", "hurt", "ache", "sore"],
            "headache": ["headache", "migraine", "head"],
            "abdominal": ["stomach", "abdominal", "belly", "gut", "tummy"],
            "rash": ["rash", "spots", "skin", "itch"],
            "vomit": ["vomit", "nause", "puke", "throw up"],
            "diarrhea": ["diarrhea", "runny", "poop"],
            "dehydration": ["thirsty", "mouth", "urine", "pee", "dehydrat"],
            "accident": ["fall", "hit", "cut", "bleed", "burn", "accident", "trauma"]
        }
        
        # Severity Modifiers
        self.severity_map = {
            "high": ["severe", "worst", "unbearable", "high", "extreme", "bad", "lot"],
            "medium": ["moderate", "medium", "quite"],
            "low": ["mild", "bit", "low", "slight", "little"]
        }

    def parse_symptoms(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        found_symptoms = []
        severity = "unknown"
        
        # Detect symptoms
        for key, patterns in self.symptoms_map.items():
            if any(p in text_lower for p in patterns):
                found_symptoms.append(key)
                
        # Detect severity
        for level, words in self.severity_map.items():
            if any(w in text_lower for w in words):
                severity = level
                break # Take highest found priority? Actually map order matters if we iterate high to low
        
        # Specific numeric checks (e.g. fever > 39)
        # Simple extraction
        temp_match = re.search(r"(\d{2}[.,]?\d?)", text) # 38, 38.5, 39
        temp = None
        if temp_match:
            try:
                temp = float(temp_match.group(1).replace(",", "."))
            except:
                pass
                
        duration_days = 0
        dur_match = re.search(r"(\d+)\s*(day|week|month)", text_lower)
        if dur_match:
            val = int(dur_match.group(1))
            unit = dur_match.group(2)
            if "week" in unit: val *= 7
            if "month" in unit: val *= 30
            duration_days = val
            
        return {
            "symptoms": found_symptoms,
            "severity": severity,
            "temperature": temp,
            "duration_days": duration_days
        }

    def triage(self, text: str) -> Dict[str, Any]:
        """
        Returns {
            'urgency': 'emergency' | 'urgent' | 'routine' | 'self_care' | 'unknown',
            'symptom_tags': [],
            'recommended_action': str,
            'follow_up_questions': [],
            'reason': str
        }
        """
        data = self.parse_symptoms(text)
        symptoms = data["symptoms"]
        severity = data["severity"]
        temp = data["temperature"]
        days = data["duration_days"]
        
        urgency = "unknown"
        questions = []
        action = "Please provide more details."
        reason = "Symptoms unclear."

        # 1. Unknown / Vague
        if not symptoms:
            return {
                "urgency": "unknown",
                "symptom_tags": [],
                "recommended_action": "I need more information to help you safely.",
                "follow_up_questions": [
                    "What are your main symptoms?",
                    "How long have you felt this way?",
                    "Do you have any pain or fever?"
                ],
                "reason": "No specific symptoms detected."
            }

        # 2. EMERGENCY Signals (Secondary check, Safety Service is primary)
        # Note: We rely on SafetyService for true emergencies (stroke, etc).
        # But here we catch high fever + stiffness, etc.
        is_child = "child" in text.lower() or "baby" in text.lower() or "kid" in text.lower()
        
        # 3. Rules Engine
        
        # Rule: High Fever
        if "fever" in symptoms:
            if temp and temp > 39.0 and not is_child: # Adult high fever
                urgency = "urgent"
                reason = f"High fever ({temp}C)."
                action = "This requires medical attention."
            elif temp and temp > 38.0 and is_child:
                urgency = "urgent"
                reason = f"Fever in child ({temp}C)."
            elif "stiffness" in text.lower() or "neck" in text.lower():
                urgency = "emergency" # Potential meningitis
                reason = "Fever with stiff neck."
                action = "Go to ER immediately."
            elif days > 3:
                urgency = "urgent"
                reason = "Persistent fever > 3 days."
            else:
                urgency = "self_care"
                reason = "Mild fever likely viral."
                action = "Monitor temperature and stay hydrated."
                questions = ["How high is the fever?", "How long have you had it?", "Do you have a stiff neck or rash?"]

        # Rule: Breathing
        if "breathing" in symptoms:
            if severity == "high" or "hard" in text.lower() or "fight" in text.lower():
                 urgency = "emergency"
                 reason = "Severe difficulty breathing."
            else:
                 urgency = "urgent"
                 reason = "Breathing difficulty."
                 questions = ["Do you have chest pain?", "Is it harder to breathe when lying down?", "do you have blue lips?"]

        # Rule: Pain
        if "pain" in symptoms or "headache" in symptoms or "abdominal" in symptoms:
            if severity == "high":
                urgency = "urgent" # Or emergency depending on location
                if "chest" in text.lower(): urgency = "emergency"
                if "headache" in symptoms and "sudden" in text.lower(): urgency = "emergency"
                reason = "Severe pain reported."
            elif days > 7:
                urgency = "routine"
                reason = "Chronic/Persistent pain."
            else:
                urgency = "self_care" if severity == "low" else "urgent"
                reason = "Moderate pain."
                
            if urgency == "urgent" or urgency == "self_care":
                questions = ["Where exactly is the pain?", "On a scale of 1-10, how bad is it?", "Did it start suddenly?"]

        # 4. Default if not caught above but symptoms exist
        if urgency == "unknown":
            # If we found symptoms but didn't match specific rules
            if severity == "high":
                urgency = "urgent"
                reason = "Severe symptoms reported."
            elif days > 7:
                urgency = "routine"
                reason = "Long-standing symptoms."
            else:
                urgency = "self_care" # Default to careful self care
                reason = "Mild symptoms detected."
                questions = ["Has this happened before?", "Are you taking any medication?", "Any other symptoms?"]

        # 5. Question Limiter
        if len(questions) > 3:
            questions = questions[:3]

        return {
            "urgency": urgency,
            "symptom_tags": symptoms,
            "recommended_action": action,
            "follow_up_questions": questions,
            "reason": reason
        }

triage_service = TriageService()
