import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import BREED_REGION_MAP_PATH

class BreedLookupService:
    def __init__(self):
        self.breed_map = {}
        self.all_breeds = []
        self._load_data()

    def _load_data(self):
        if not BREED_REGION_MAP_PATH.exists():
            print(f"Warning: Breed region map not found at {BREED_REGION_MAP_PATH}")
            return
            
        with open(BREED_REGION_MAP_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        self.all_breeds = data
        # Lowercase keys for fuzzy matching
        for item in data:
            key = f"{item['type']}_{item['breed'].lower()}"
            self.breed_map[key] = item
            
            # also index by just breed name
            key_breed_only = item['breed'].lower()
            if key_breed_only not in self.breed_map:
                self.breed_map[key_breed_only] = item
            else:
                # If there's a conflict (like Bargur), this simple dict entry gets overwritten.
                pass

    def get_region(self, breed_name: str, animal_type: str = None) -> dict:
        """
        Given a breed name and optional type, return the region data.
        Returns "Data unavailable" for unknown breeds.
        """
        breed_lower = breed_name.lower()
        
        if animal_type:
            key = f"{animal_type.lower()}_{breed_lower}"
            if key in self.breed_map:
                return self.breed_map[key]
                
        if breed_lower in self.breed_map:
            return self.breed_map[breed_lower]
            
        return {
            "breed": breed_name,
            "native_region": ["Data unavailable"],
            "type": animal_type or "unknown"
        }

    def get_all_breeds(self):
        return self.all_breeds

# Singleton instance
breed_lookup = BreedLookupService()
