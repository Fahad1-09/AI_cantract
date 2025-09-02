from pathlib import Path
import google.generativeai as genai

PROMPT_FILE = Path(__file__).resolve().parent.parent / "prompts" / "summary_prompts.txt"
SUMMARY_PROMPT = PROMPT_FILE.read_text(encoding="utf-8")

def generate_summary(contract_text: str) -> str:
    prompt = SUMMARY_PROMPT.format(contract=contract_text)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()
