# -*- encoding: utf-8 -*-
import plotly
import plotly.graph_objs as go
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from apps.home import dataDf


map_months = {1: "Janeiro",
              2: "Fevereiro",
              3: "Março",
              4: "Abril",
              5: "Maio",
              6: "Junho",
              7: "Julho",
              8: "Agosto",
              9: "Setembro",
              10: "Outubro",
              11: "Novembro",
              12: "Dezembro"}


def daily_trips():
    pv = dataDf.groupby(["Ano do Início Viagem", "Mês do Início Viagem"])[
        "Viagem"].count().reset_index()

    pv = pd.pivot_table(pv, index="Mês do Início Viagem",
                        columns="Ano do Início Viagem", values='Viagem')
    pv.index = pv.index.map(map_months)

    fig = px.line(pv)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
