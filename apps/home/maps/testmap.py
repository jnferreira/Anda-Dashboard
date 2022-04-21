import folium

# TODO Converter o geopandas dataframe para um .h5 e carregar aqui


def saveFoliumMapTest():
    start_coords = (46.9540700, 142.7360300)
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    return folium_map._repr_html_()
