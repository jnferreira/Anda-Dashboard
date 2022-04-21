# -*- encoding: utf-8 -*-
from lib2to3.pgen2.pgen import DFAState
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


def profiles():
    df = dataDf.groupby(["Perfil Social"])["Viagem"].count().reset_index()

    fig = px.pie(df, values='Viagem', names='Perfil Social')
    fig.update_traces(textposition='inside', textinfo='percent+label')

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


def totalByHourAndWeekday():
    arr = dataDf.groupby(["Hora do Início Viagem", "Dia da Semana do Início Viagem"])[
        'Viagem'].count().reset_index()
    fig = px.line(arr, x=arr['Hora do Início Viagem'],
                  y=arr["Viagem"], color=arr["Dia da Semana do Início Viagem"])
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


def profilesByMonth(year=2019):
    df = dataDf.loc[(dataDf["Ano do Início Viagem"] == year)]

    df = df.groupby(["Perfil Social", "Mês do Início Viagem"])[
        "Viagem"].count().reset_index()
    pv = pd.pivot_table(df, index="Perfil Social",
                        columns="Mês do Início Viagem", values='Viagem')

    fig = px.bar(pv, barmode='group')
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
