import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=[1, 2, 3, 4, 5],
        y=[10, 20, 15, 30, 25],
        mode="lines+markers",
        name="Результат",
    )
)

fig.update_layout(
    title="Интерактивный результат эксперимента",
    xaxis_title="Параметр",
    yaxis_title="Значение",
    showlegend=True,
)

fig.write_html(
    "plotly_graph.html",
    full_html=True,
    include_plotlyjs=True,
)

fig.write_html(
    "plotly_fragment.html",
    full_html=False,
    include_plotlyjs=True,
)