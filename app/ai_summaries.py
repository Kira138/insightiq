# ============================================================
# InsightIQ — AI Summaries
# Uses Claude API to generate KPI insights
# ============================================================
import anthropic
import os

# ── INITIALIZE CLIENT ─────────────────────────────────────
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# ── GENERATE KPI SUMMARY ──────────────────────────────────
def generate_kpi_summary(kpi_name, current_value, delta, context=""):
    prompt = f"""
    You are a business analyst. Write a 2-sentence executive summary for this KPI:
    
    KPI: {kpi_name}
    Current Value: {current_value}
    Change: {delta}%
    Context: {context}
    
    Be concise, business-focused, and actionable.
    """
    
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text

if __name__ == "__main__":
    summary = generate_kpi_summary("Revenue", "R$ 985,414", -4.1)
    print(summary)