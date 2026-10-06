from fastapi import FastAPI
from app_logging import get_logger
from agents.diet_agent import DietAgent
from agents.inventory_agent import InventoryAgent
from agents.manager_agent import ManagerAgent
from agents.planner_agent import PlannerAgent
from models import (
    AskInput, AskResponse, DietInput, DietResponse, InventoryInput, InventoryResponse,
    PlanInput, RecipeResponse, RecommendInput, RecommendResponse,
)

logger = get_logger("app")
app = FastAPI(title="AI Diet & Meal Planner")


@app.get("/")
def root():
    return {"message": "Success!"}


@app.post("/inventory", response_model=InventoryResponse)
def inventory(data: InventoryInput):
    return InventoryAgent().run(data.items)


@app.post("/diet", response_model=DietResponse)
def diet(data: DietInput):
    return DietAgent().run(data.items, data.diet)


@app.post("/ask", response_model=AskResponse)
def ask(data: AskInput):
    logger.info("Received /ask request: items=%s, diet=%s", data.items, data.diet)
    result = ManagerAgent().run(data.items, data.diet)
    logger.info("/ask response: suggestions=%s", result.suggestions)
    return result


@app.post("/plan", response_model=RecipeResponse)
def plan(data: PlanInput):
    logger.info("Received /plan request: base_recipe=%s", data.base_recipe)
    result = PlannerAgent().run(data.base_recipe)
    logger.info("/plan response: title=%s", result.title)
    return result


@app.post("/recommend", response_model=RecommendResponse)
def recommend(data: RecommendInput):
    logger.info(
        "Received /recommend request: items=%s, diet=%s, recipe_count=%s",
        data.items, data.diet, data.recipe_count,
    )
    ask_result = ManagerAgent().run(data.items, data.diet)
    planner = PlannerAgent()
    recipes = [planner.run(idea) for idea in ask_result.suggestions[: data.recipe_count]]
    logger.info("/recommend response: %s recipes returned", len(recipes))
    return RecommendResponse(recipes=recipes)