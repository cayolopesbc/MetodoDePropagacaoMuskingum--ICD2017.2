from env_django import run_env_django

run_env_django()
import os
import comtypes.client
from ICDR.models import *
import django
import pandas as pd
import numpy as np
from datetime import datetime
django.setup()


#ADD Informações de postos no banco de dados
def create_station(station_infos_path,data_dir):
    station_infos = pd.read_excel(station_infos_path)
    for station_code in station_infos['Codigo']:
        station = Station.objects.filter(code = station_code)
        if station[0]:
            get_serie_from_txt(str(station_code),station[0], data_dir)
            print('Série de dados da estação '+str(station_code) + ' atualizada.')
        else: 
            station_info = station_infos.loc[station_infos['Codigo'] == station_code]
            coord = Coordinate.objects.create(y = station_info['Latitude'], x = station_info['Longitude'])
            station = Station.objects.create(name = station_info['Nome'].values[0], code =  station_code, coordinates = coord, drainarea = station_info['AreaDrenag'])
            get_serie_from_txt(str(station_code),station, data_dir)
            print(str(station_code) + ' criada.')


def get_serie_from_txt(station,station_obj, DATA_DIR = None):
    
    #Características do dado a ser análisado
    data_type = ['Nível.txt','Níveis','cm']

    #Loop através dos nomes dos arquivos, buscando
    #os arquivos que contém os dados de cota dos postos

    for file in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR,file)
        if file_path.split('\\')[len(file_path.split('\\'))-1].count(station[1:8]) and file_path.count(data_type[0][0:4]):
            with open(file_path) as file:
                file.readline()
                obj = []
                for line in file.readlines():
                    line = line.split()
                    if len(line)==3:
                        date,hour,data = line
                    else:
                        date,hour = line
                        data = np.nan
                    date_and_hour = datetime.strptime("%s %s"%(date,hour), '%d/%m/%Y %H:%M:%S')
                    obj.append(DataSerie(data = data, date = date_and_hour, station = station_obj))
            DataSerie.objects.bulk_create(obj)



if __name__ == '__main__':
    station_infos = os.path.join(os.getcwd(),'DadosDeEntrada\\est_fluvio.xls')
    data_dir =  os.path.join(os.getcwd(),'DadosDeEntrada')
    create_station(station_infos,data_dir)
