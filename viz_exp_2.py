import plotly.express as px
import pandas as pd
import plotly.io as pio

# Experiment 1
df = pd.read_csv('./data/exp-2.csv')
print(df)
df['time_performance'] = df['time_performance']/1000
df['time_performance'].round(3)
df['conflct_ratio'] = (df['conflct_ratio']*100).astype(int)
df['conflct_ratio'] = df['conflct_ratio'].astype(str) + '%'
 
box1 = px.box(df, x="conflct_ratio", y="time_performance")
box2 = px.box(df, x="conflct_ratio", y="makespan")

box1.update_layout(
    height=1000, 
    width=1000,
    title="(a)",
    xaxis_title="Action Conflict",
    yaxis_title="Runtime (s)",
    font=dict(
        family="Arial Black",
        size=8,
        color="Black"
    )
)
box2.update_layout(
    height=1000, 
    width=1000,
    title="(b)",
    xaxis_title="Action Conflict",
    yaxis_title="Makespan",
    font=dict(
        family="Arial Black",
        size=8,
        color="Black"
    )
)

pio.write_image(box1, 'exp_2-runtime.svg')
pio.write_image(box2, 'exp_2-makespan.svg')
