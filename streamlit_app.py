import streamlit as st
import streamlit.components.v1 as components

from agents.manager_agent import ManagerAgent
from agents.parser_agent import ParserAgent
from agents.planner_agent import PlannerAgent
from services.llm_client import LLMClient

RECIPE_COUNT = 3


def format_reply(parsed, ask_result, recipes):
    lines = [
        f"**Diet:** {parsed.diet}",
        f"**Ingredients that fit:** {', '.join(ask_result.diet_filtered)}",
        "",
    ]
    for recipe in recipes:
        lines.append(f"### {recipe.title}")
        lines.append("**Ingredients:** " + ", ".join(recipe.ingredients))
        lines.append("")
        for step in recipe.steps:
            lines.append(f"{step.step_number}. {step.instruction}")
        lines.append("")
    return "\n".join(lines)


SCROLL_SCRIPT = """
<script>
setTimeout(function () {
    const bubbles = window.parent.document.querySelectorAll('[data-testid="stChatMessage"]');
    if (bubbles.length > 0) {
        bubbles[bubbles.length - 1].scrollIntoView({behavior: "smooth", block: "start"});
    }
}, 100);
</script>
"""


def scroll_to_latest_message():
    marker = f"<!-- {len(st.session_state.messages)} -->"
    components.html(SCROLL_SCRIPT + marker, height=0)


st.set_page_config(page_title="AI Diet & Meal Planner")
st.title("AI Diet & Meal Planner")
st.caption("Tell me what ingredients you have and what diet you follow.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

submission = st.chat_input(
    "Type or record your ingredients and diet...",
    accept_audio=True,
)

message = None
if submission:
    if submission.audio:
        with st.spinner("Transcribing..."):
            message = LLMClient().transcribe(submission.audio.getvalue())
    else:
        message = submission.text

if message:
    st.session_state.messages.append({"role": "user", "content": message})
    with st.chat_message("user"):
        st.markdown(message)
    scroll_to_latest_message()

    with st.chat_message("assistant"):
        with st.spinner("Planning recipes..."):
            parsed = ParserAgent().run(message)
            ask_result = ManagerAgent().run(parsed.items, parsed.diet)
            planner = PlannerAgent()
            recipes = [
                planner.run(idea, ask_result.diet_filtered)
                for idea in ask_result.suggestions[:RECIPE_COUNT]
            ]
        reply = format_reply(parsed, ask_result, recipes)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    scroll_to_latest_message()