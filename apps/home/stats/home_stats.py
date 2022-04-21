# -*- encoding: utf-8 -*-
import plotly
import plotly.graph_objs as go
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from apps.home import dataDf


def total_trips():
    return len(dataDf)


def total_users():
    return dataDf["UserHash"].nunique()
