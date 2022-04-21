from apps.home import blueprint
from flask import render_template, request
from jinja2 import TemplateNotFound
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from apps.home import dataDf
from apps.home.plots.daily_trips import *
from apps.home.maps.testmap import *


# TESTING STUFF
def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig


@blueprint.route('/')
def index():
    test = 1
    return render_template('home/index.html', segment='index', plot=daily_trips(), test=test, data_df=dataDf, map=saveFoliumMapTest())


@blueprint.route('/geo')
def geoRounting():
    return render_template('home/geo.html', segment='geo', map=saveFoliumMapTest())


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
