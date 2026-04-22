# ============================================================
# InsightIQ — AI Summaries
# Uses Claude API to generate KPI insights
# ============================================================
import anthropic
import os
from dotenv import load_dotenv

# ── INITIALIZE CLIENT, Setup (runs once at import time) ─────────────────────────────────────
load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ── GENERATE KPI SUMMARY,Three values get passed in — kpi_name, current_value, delta. context defaults to "" since it wasn't provided. ──────────────────────────────────
def generate_kpi_summary(kpi_name, current_value, delta, context=""):
#Claude receives this as its instruction giving it the role of a business analyst and telling it exactly what to write.
    prompt = f"""   
    You are a business analyst. Write a 2-sentence executive summary for this KPI:
    
    KPI: {kpi_name}
    Current Value: {current_value}
    Change: {delta}%
    Context: {context}
    
    Be concise, business-focused, and actionable.
    """
#── prompt is sent to Claude Haiku. Claude reads it and generates a 2-sentence executive summary, capped at 150 tokens.
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text

if __name__ == "__main__":
    summary = generate_kpi_summary("Revenue", "R$ 985,414", -4.1)
    print(summary)