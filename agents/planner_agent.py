import json
from typing import Any, List, Optional

from models import RecipeResponse, RecipeStep
from services.llm_client import LLMClient


class PlannerAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, base_recipe: str, available_items: Optional[List[str]] = None) -> RecipeResponse:
        ingredient_rule = ""
        if available_items:
            ingredient_rule = (
                f"Use ONLY these ingredients: {json.dumps(available_items)}.\n"
                "You may also use these basic pantry staples: salt, pepper, cooking oil, water.\n"
                "Do not use any other ingredients, even if the meal idea's name suggests them.\n"
            )
        prompt = (
            "You are a chef. Write a complete recipe for this meal idea:\n"
            f"{base_recipe}\n"
            f"{ingredient_rule}"
            "Return a JSON object with exactly these fields:\n"
            "  title: a string, the recipe name,\n"
            "  ingredients: an array of strings, one ingredient per string,\n"
            "  steps: an array of objects, each with step_number (an integer starting at 1) "
            "and instruction (a string).\n"
            "Respond ONLY with valid JSON."
        )
        result = self.llm.call_model_json(prompt)
        return RecipeResponse(
            title=str(result.get("title", base_recipe)),
            ingredients=self._normalize_ingredients(result.get("ingredients", [])),
            steps=self._normalize_steps(result.get("steps", [])),
        )

    def _normalize_ingredients(self, raw: List[Any]) -> List[str]:
        ingredients = []
        for item in raw:
            if isinstance(item, dict):
                ingredients.append(str(item.get("name", item)))
            else:
                ingredients.append(str(item))
        return ingredients

    def _normalize_steps(self, raw: List[Any]) -> List[RecipeStep]:
        steps = []
        for number, step in enumerate(raw, start=1):
            if isinstance(step, dict):
                instruction = str(step.get("instruction", step))
            else:
                instruction = str(step)
            steps.append(RecipeStep(step_number=number, instruction=instruction))
        return steps