import json

from models import ParsedRequest
from services.llm_client import LLMClient


class ParserAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, message: str) -> ParsedRequest:
        prompt = (
            "You read a message from someone asking for recipe ideas. "
            "The message may be dictated speech, so it can be informal.\n"
            f"Message: {json.dumps(message)}\n"
            "Return a JSON object with:\n"
            "  items: an array of the ingredients the person says they have, one ingredient per string, "
            'using simple names without quantities (for example "bell pepper", not "two bell peppers"),\n'
            "  diet: the diet the person says they follow, as a short lowercase string "
            '(for example "vegan" or "keto"), or "no restrictions" if they do not mention one.\n'
            "Respond ONLY with valid JSON."
        )
        result = self.llm.call_model_json(prompt)
        items = [str(item) for item in result.get("items", [])]
        diet = str(result.get("diet") or "no restrictions")
        return ParsedRequest(items=items, diet=diet)