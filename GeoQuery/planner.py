from pathlib import Path
from llm import llm

PROMPT = Path(
    "prompts/planner.txt"
).read_text()

def create_plan(question):
    response = llm.invoke(
        PROMPT + "\n\nUser:\n" + question
    )

    return response.content