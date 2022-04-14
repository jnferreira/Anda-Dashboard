from apps.home import blueprint
from flask import render_template, request
from jinja2 import TemplateNotFound
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
from matplotlib import pyplot as plt
import datetime
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import folium


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


def preprocessData(data_df):
    # Removido as validações com o valor "Card4B" no atributo "Grupo do Cliente"
    data_df.drop(
        data_df.index[data_df['Grupo do Cliente'] == 'Card4B'], inplace=True)
    data_df["Hora Início Viagem"] = pd.to_datetime(
        data_df['Hora Início Viagem'], format="%Y-%m-%d %H:%M:%S")
    data_df["Hora Fim Viagem"] = pd.to_datetime(
        data_df['Hora Fim Viagem'], format="%Y-%m-%d %H:%M:%S")
    data_df["Hora Início Etapa"] = pd.to_datetime(
        data_df['Hora Início Etapa'], format="%Y-%m-%d %H:%M:%S")
    data_df["Hora Fim Etapa"] = pd.to_datetime(
        data_df['Hora Fim Etapa'], format="%Y-%m-%d %H:%M:%S")
    data_df["Ano do Início Viagem"] = data_df["Hora Início Viagem"].dt.year
    data_df["Mês do Início Viagem"] = data_df["Hora Início Viagem"].dt.month
    data_df["Dia do Início Viagem"] = data_df["Hora Início Viagem"].dt.day
    data_df["Dia da Semana do Início Viagem"] = data_df["Hora Início Viagem"].dt.day_name()
    data_df["Hora do Início Viagem"] = data_df["Hora Início Viagem"].dt.hour

    return data_df


def getData():
    data_df = pd.read_hdf('./data.h5')
    data_df = preprocessData(data_df)
    return data_df


def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig


def create_plot():

    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y})  # creating a sample dataframe

    data = [
        go.Bar(
            x=df['x'],  # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

# TODO Converter o geopandas dataframe para um .h5 e carregar aqui


def saveFoliumMapTest():
    start_coords = (46.9540700, 142.7360300)
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    return folium_map._repr_html_()


def first_plot():
    data_df = getData()
    pv = data_df.groupby(["Ano do Início Viagem", "Mês do Início Viagem", "Dia do Início Viagem"])[
        'Viagem'].count().reset_index()
    pv = pv.groupby(["Ano do Início Viagem", "Mês do Início Viagem"])[
        "Viagem"].mean().reset_index()

    pv = pd.pivot_table(pv, index="Mês do Início Viagem",
                        columns="Ano do Início Viagem", values='Viagem')
    pv.index = pv.index.map(map_months)

    fig = px.line(pv)
    # return  html.Div([dcc.Graph(figure=fig)])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@blueprint.route('/')
def index():
    map = saveFoliumMapTest()
    bar = first_plot()
    test = 1
    data_df = getData()
    return render_template('home/index.html', segment='index', plot=bar, test=test, data_df=data_df, map=map)
    # return render_template('home/index.html', segment='index', plot=bar)


@blueprint.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@blueprint.route('/<template>')
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
