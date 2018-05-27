import json
import numpy as np
import folium
import os

def plot_map(stretch_data):
    
    coordinates = stretch_data['upstream'][1]['Coordinates']
    Map = folium.Map(coordinates, zoom_start = 10)
    base = os.getcwd()
    keys = ['upstream','downstream']

    for station in keys:
        station_infos = stretch_data[station][1]
        station_coordinates = [station_infos['Coordinates'][0], station_infos['Coordinates'][1]]

        html_info = """
        <h5> <b>Dados do Posto</b></h5>
        <p> <big><b>Nome: </b>{}<\p>
        <p> <b>Código: </b>{}<\p>
        <p> <b>Área de drenagem: </b> {} km<sup>2<\sup> <\p>
        <p> <b>Latitude: </b>{} <sup>o<\sup><\p>
        <p> <b>Longitude: </b> {} <sup>o<\sup><\p>
        """.format(
            station_infos['Name'].upper(),
            station_infos['Code'],
            station_infos['DrainArea'], 
            station_infos['Coordinates'][0],
            station_infos['Coordinates'][1],
            )

        folium.Marker(station_coordinates, popup = html_info).add_to(Map)

    return Map
