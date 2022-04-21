# -*- encoding: utf-8 -*-
from flask import Blueprint
import pandas as pd


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


dataDf = getData()

blueprint = Blueprint(
    'home_blueprint',
    __name__,
    url_prefix=''
)
