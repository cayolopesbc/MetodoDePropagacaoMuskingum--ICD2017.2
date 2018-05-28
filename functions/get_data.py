from numpy import matrix, nan
import os
import pandas as pd
import numpy as np
from datetime import datetime
from collections import OrderedDict
from ICDR.models import *

#Função para pegar informações sobre os postos do banco de dados
def get_station_info(station_code):
    station = Station.objects.filter(code = station_code)
    if station:
        station_info = station[0]
        station_info = {
            'Name': station_info.name,
            'Code': station_info.code,
            'Coordinates':[station_info.coordinates.y,
            station_info.coordinates.x],
            'DrainArea': station_info.drainarea,
        }   
    else:
            station_info = {
            'Name': 'Informação não encontrada',
            'Code': station_info.code,
            'Coordinates':[np.nan,
            np.nan],
            'DrainArea': 'Informação não encontrada',
        }  

    return station_info

#Funçao que auxilia a leitura de dados oriundos de arquivos .txt
def get_station_data(file_path,station_list,data_type,station_data,f):

    for station in station_list:

        if file_path.split('\\')[len(file_path.split('\\'))-1].count(station[1:8]) and file_path.count(data_type[0][0:4]):
            data = pd.read_csv(file_path,
            skiprows = 1, 
            names = ['Dates','Data'],
            dtype = {'Dates':datetime,'Data':np.float},
            sep = '                 ',
            engine = 'python') 
            
            data['Dates'] = pd.to_datetime(data['Dates'],
            errors ='coerce', 
            format ='%d/%m/%Y %H:%M:%S')
            
            data = data.set_index(['Dates']).groupby(pd.TimeGrouper(freq = f)).mean().reset_index()
           
        
            info = get_station_info(station)

            info['DataType'] = data_type[1:]
            station_data.append([station,[data,info]])

    return station_data

#Função para entrada de Dados tipo: DATA/HORA - DADO de um conjunto de arquivos .txt

def data_read_from_txt(file_station = None, DATA_DIR = None,tp = None,f = '0.25H'):
    
    #Abre arquivo com a lista de postos
    with open(file_station,'r') as stations:
        station_list = stations.read().split()

    #Características do dado a ser análisado
    data_type = ['Nível.txt','Níveis','cm']

    #Loop através dos nomes dos arquivos, buscando
    #os arquivos que contém os dados de cota dos postos
    station_data = []
    no_tp_data=[]

    for file in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR,file)
        station_data,station_in = get_station_data(file_path, station_list, data_type,station_data,f)
    station_data = OrderedDict(station_data)
    
    # Verifica quais postos não apresentam
    for station in station_list:
        if station not in station_data.keys():
            no_tp_data.append(station)        
    
    if len(no_tp_data)!=0:
        print("Não foram encontrados dados de ", data_types[tp][0]," para: \n")
        for no in no_tp_data:
            print(no +'\n')
    print('Dados de entrada - ok.')
    return station_data


#Função que pega do banco de dados as séries históricas de  Dados tipo: DATA/HORA - DADO
#além de informações sobre os postos
def data_read_from_db(file_station = None, f = '0.25H'):

    #Abre arquivo com a lista de postos:
    with open(file_station,'r') as stations:
        station_list = stations.read().split()

    #Características do dado a ser análisado:
    data_type = ['Nível.txt','Níveis','cm']
    station_data =[]

    #Pega dados do banco de dados:
    for station_code in station_list:
        station = Station.objects.filter(code = station_code)[0]
        data = DataSerie.objects.filter(station = station)
        data_st = []
        dates_st = []
        for i in range(len(data)):
            data_st.append(data[i].data)
            dates_st.append(data[i].date)
        data = pd.DataFrame.from_dict({'Data': data_st, 'Dates': dates_st})
        data = data.set_index(['Dates']).groupby(pd.TimeGrouper(freq = f)).mean().reset_index()
        info = get_station_info(station_code)
        info['DataType'] = data_type[0][1:]
        station_data.append([station_code,[data,info]])
    print('Dados de entrada - ok.')
    return OrderedDict(station_data)


        

if __name__ == '__main__':
    file_path = os.path.join(os.getcwd(),'DadosDeEntrada\\PCDS.txt')
    data_path =  os.path.join(os.getcwd(),'DadosDeEntrada')
    data = data_read_from_txt(file_station = file_path, DATA_DIR = data_path, f = '0.25H')
