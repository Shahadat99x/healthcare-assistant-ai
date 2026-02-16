import json
import re
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path

# Path to local data
DATA_PATH = Path(__file__).parent.parent.parent.parent / "data" / "local" / "bucharest_hospitals.json"

class LogisticsService:
    def __init__(self):
        self.resources = []
        self._load_data()
        
    def _load_data(self):
        """Loads the local dataset into memory."""
        try:
            if DATA_PATH.exists():
                with open(DATA_PATH, "r", encoding="utf-8") as f:
                    self.resources = json.load(f)
                print(f"[Logistics] Loaded {len(self.resources)} resources from {DATA_PATH}")
            else:
                print(f"[Logistics] Warning: Data file not found at {DATA_PATH}")
                self.resources = []
        except Exception as e:
            print(f"[Logistics] Error loading data: {e}")
            self.resources = []

    def _extract_sector(self, text: str) -> Optional[int]:
        """
        Deterministically extracts sector number from text.
        Patterns: "sector 6", "sector six", "sect 6"
        Returns 1-6 or None.
        """
        text_lower = text.lower()
        
        # numeric matches
        match = re.search(r"\bsect(?:or)?\s*(\d)\b", text_lower)
        if match:
            s = int(match.group(1))
            if 1 <= s <= 6:
                return s
        
        # word matches
        word_map = {
            "one": 1, "two": 2, "three": 3, 
            "four": 4, "five": 5, "six": 6
        }
        for word, num in word_map.items():
            if f"sector {word}" in text_lower or f"sect {word}" in text_lower:
                return num
                
        return None

    def find_resources(self, query: str, type_filter: Optional[str] = None, limit: int = 3) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Finds resources based on query (sector, keywords) and type.
        Returns (list of resources, context dict).
        """
        sector = self._extract_sector(query)
        
        # Filter Logic
        results = self.resources
        
        # 1. Type Filter (if strict)
        if type_filter:
            results = [r for r in results if r.get("type") == type_filter]
            
        # 2. Sector Filter (if detected in query)
        if sector:
            results = [r for r in results if r.get("sector") == sector]
            
        # 3. Simple Keyword Match (if no sector specific query or to further refine)
        # If sector was found, we rely mostly on that. If not, check text.
        if not sector and not type_filter:
            # Basic keyword search if generic logistics query
            query_lower = query.lower()
            scored = []
            for r in results:
                score = 0
                if r["name"].lower() in query_lower: score += 2
                if r["address"].lower() in query_lower: score += 1
                if score > 0:
                    scored.append((score, r))
            
            # If we found matches by name, prioritise them
            if scored:
                scored.sort(key=lambda x: x[0], reverse=True)
                results = [x[1] for x in scored]

        # 4. Limit
        return results[:limit], {"city": "Bucharest", "sector": sector, "mode": "logistics"}

    def get_emergency_hospitals(self, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Return top emergency hospitals (regardless of sector, or generic recommendation).
        """
        # Prioritize major ones (usually sector 1, 5, 4 have big emergency hubs)
        # For now just filter type="emergency"
        emergencies = [r for r in self.resources if r.get("type") == "emergency"]
        return emergencies[:limit]

logistics_service = LogisticsService()
