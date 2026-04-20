from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from textwrap import wrap
from io import BytesIO

def generate_pdf(kpi_data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, 750, "InsightIQ — Executive Report")
    
    # Date range
    c.setFont("Helvetica", 12)
    c.drawString(50, 720, f"Period: {kpi_data['start_date']} to {kpi_data['end_date']}")
    
    # KPI data
    y = 680
    for kpi in kpi_data['kpis']:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, kpi['name'])
        c.setFont("Helvetica", 11)
        c.drawString(50, y-20, f"Value: {kpi['value']}  Change: {kpi['delta']}")
        
        # ← wrap long summary text!
        wrapped = wrap(kpi['summary'], width=90)
        text_y = y - 40
        for line in wrapped:
            c.drawString(50, text_y, line)
            text_y -= 15  # each line 15 points down
        
        y -= (60 + len(wrapped) * 15)  # more space for wrapped text!
    
    c.save()
    buffer.seek(0)
    return buffer