from pathlib import Path
import google.generativeai as genai

PROMPT_FILE = Path(__file__).resolve().parent.parent / "prompts" / "compliance_prompt.txt"
COMPLIANCE_PROMPT = PROMPT_FILE.read_text(encoding="utf-8")


def check_compliance(contract_text: str) -> str:
    prompt = COMPLIANCE_PROMPT.format(contract=contract_text)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()
