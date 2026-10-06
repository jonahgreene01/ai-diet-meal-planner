import json
from typing import List

from models import DietResponse
from services.llm_client import LLMClient


class DietAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, items: List[str], diet: str) -> DietResponse:
        prompt = (
            "You are a nutrition assistant. Given the JSON array of ingredients:\n"
            f"{json.dumps(items)}\n"
            f"and the diet: {diet}\n"
            "Return a JSON object with:\n"
            f"  compatible_items: an array of the ingredients from the list that fit the {diet} diet,\n"
                       "  suggested_recipe_ideas: an array of exactly 5 recipe names that can be made using ONLY the compatible items, "
            "plus basic pantry staples (salt, pepper, cooking oil, water, garlic powder, flour, hot sauce, Italian seasoning, creole seasoning, taco seasoning ).\n"
            "Respond ONLY with valid JSON."
        )
        result = self.llm.call_model_json(prompt)
        return DietResponse(**result)