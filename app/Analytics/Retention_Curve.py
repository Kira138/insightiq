import plotly.express as px
import pandas as pd
from app.kpi_engine import get_cohort_retention

def plot_retention_curve():
    df = get_cohort_retention()

    cohort_pivot = df.pivot_table(
        index='first_order_date',
        columns='cohort_month',
        values='retention_pct'
    )

    cohort_pivot_display = cohort_pivot.round(1)

    fig = px.imshow(                #tells Plotly to make an image/heatmap from a 2D data structure
        cohort_pivot_display,        #the data going in   
        labels=dict(x="Cohort Month", y="First Order Month", color="Retention %"), #labels=dict(...)-renames the axes and color bar in the chart
        title="Customer Retention Cohort Analysis",
        color_continuous_scale="Greens",
        aspect="auto"
    )

    fig.update_traces(                   #modifies how the chart behaves after it's been created
        hoverongaps=False,  #Controls what happens when you hover over an empty cell (NaN — the staircase region),   
        #hoverongaps=True  → shows tooltip saying "Retention %: NaN"  ← ugly ,hoverongaps=False → shows nothing on empty cells             ← clean           
        hovertemplate="Cohort Month: %{x}<br>First Order Month: %{y}<br>Retention: %{z:.1f}%<extra></extra>"
    )

    fig.show()

if __name__ == "__main__":
    plot_retention_curve()

    #Function is called (via if __name__ == "__main__")
    #get_cohort_retention() — fetches raw data from kpi_engine, returns a flat table
    #pivot_table() — reshapes that flat table into a date × cohort_month grid
    #.round(1) — trims decimals for clean tooltip display
    #px.imshow() — takes the grid and builds a Plotly heatmap figure
    #update_traces() — patches the figure: silence NaN cells, format hover text
    #fig.show() — renders it in the browser