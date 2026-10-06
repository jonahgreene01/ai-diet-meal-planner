from typing import List

from agents.diet_agent import DietAgent
from agents.inventory_agent import InventoryAgent
from models import AskResponse


class ManagerAgent:
    def __init__(self):
        self.inventory_agent = InventoryAgent()
        self.diet_agent = DietAgent()

    def run(self, items: List[str], diet: str) -> AskResponse:
        inventory_result = self.inventory_agent.run(items)
        diet_result = self.diet_agent.run(inventory_result.usable_items, diet)
        return AskResponse(
            usable_items=inventory_result.usable_items,
            diet_filtered=diet_result.compatible_items,
            suggestions=diet_result.suggested_recipe_ideas,
        )