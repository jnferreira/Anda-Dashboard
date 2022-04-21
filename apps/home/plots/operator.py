# -*- encoding: utf-8 -*-
import plotly
import plotly.graph_objs as go
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from apps.home import dataDf


def operators_perc():
    pv = dataDf.groupby("Operador")["Viagem"].count(
    ).reset_index().sort_values(by="Viagem", ascending=False)
    fig = px.bar(pv, x="Operador", y="Viagem", barmode='group')
    fig.add_trace(
        go.Scatter(
            name="Total de viagens",
            x=pv["Operador"],
            y=pv["Viagem"]
        ))

    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    fig.update_layout(
        font_color="white",
        title_font_color="white",
        legend_title_font_color="white"
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
