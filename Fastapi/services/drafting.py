
import google.generativeai as genai
from pathlib import Path

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "contract_prompt.txt"
with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    BASE_PROMPT = f.read()

def generate_draft(chunks: list, user_data: dict) -> str:
    # Base contract as structure
    reference_text = "\n\n".join(chunks)

    # Fill placeholders
    prompt = BASE_PROMPT.format(
        company_name=user_data.get("company_name", ""),
        project_name=user_data.get("project_name", ""),
        project_scope=user_data.get("project_scope", ""),
        tools=user_data.get("tools", ""),
        duration=user_data.get("duration", ""),
        deliverables=user_data.get("deliverables", "")
    )

    final_prompt = prompt + "\n\nUse this contract as structure:\n" + reference_text

    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(final_prompt)
    return response.text
