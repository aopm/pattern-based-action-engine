import plotly.express as px
import pandas as pd
import plotly.io as pio

# Experiment 1
df = pd.read_csv('./data/exp-1.csv')
df['time_performance'] = df['time_performance']/1000
df['time_performance'].round(3)
df['conflct_ratio'] = (df['conflct_ratio']*100).astype(int)
df['conflct_ratio'] = df['conflct_ratio'].astype(str) + '%'
print(df)
line1 = px.line(df, x='num_actions', y='time_performance', color='conflct_ratio', markers=True)
line2 = px.line(df, x='num_actions', y='makespan', color='conflct_ratio', markers=True)
line3 = px.line(df, x='conflct_ratio', y='time_performance', color='num_actions', markers=True)
line4 = px.line(df, x='conflct_ratio', y='makespan', color='num_actions', markers=True)

line1.update_layout(
    height=500, 
    width=400,
    title="(a)",
    xaxis_title="# Actions in Action Requirement",
    yaxis_title="Runtime (s)",
    legend_title="Action<br>Conflict",
    font=dict(
        family="Arial Black",
        size=8,
        color="Black"
    ),
    xaxis=dict(
        dtick=100)
)

line2.update_layout(
    height=500, 
    width=400,
    title="(c)",
    xaxis_title="# Actions in Action Requirement",
    yaxis_title="Makespan",
    legend_title="Action<br>Conflict",
    font=dict(
        family="Arial Black",
        size=8,
        color="Black"
    ),
    xaxis=dict(
        dtick=100)
)

line3.update_layout(
    height=500, 
    width=400,
    title="(b)",
    xaxis_title="Action Conflict",
    yaxis_title="Runtime (s)",
    legend_title="# Actions",
    font=dict(
        family="Arial Black",
        size=8,
        color="Black"
    )
)

line4.update_layout(
    height=500, 
    width=400,
    title="(d)",
    xaxis_title="Action Conflict",
    yaxis_title="Makespan",
    legend_title="# Actions",
    font=dict(
        family="Arial Black",
        size=8,
        color="Black"
    )
)

pio.write_image(line1, './chart/exp1-1-makespan.svg', width=400, height=500)
pio.write_image(line2, './chart/exp1-2-makespan.svg', width=400, height=500)
pio.write_image(line3, './chart/exp1-1-runtime.svg', width=400, height=500)
pio.write_image(line4, './chart/exp1-2-runtime.svg', width=400, height=500)
