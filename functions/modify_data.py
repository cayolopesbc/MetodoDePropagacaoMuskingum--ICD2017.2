from datetime import datetime
from numpy import nan
import os
import pandas as pd
from collections import OrderedDict

def convert_date(date):
    try:
        date = datetime.strptime(date,"%d-%m-%Y-%H-%M")
    except:
        date_split = date.split('-')
        while len(date_split) < 5:
            date +='-00'
            date_split = date.split('-')
        date = datetime.strptime(date,"%d-%m-%Y-%H-%M")
    return date

#Separa um evento em determinado período
def get_data_event(station_data,period = None):
    start_date = convert_date(period[0])
    end_date = convert_date(period[1])
    event_data = []
    for station in station_data.keys():
        try:
            data = station_data[station][0].set_index('Dates').loc[start_date:end_date].reset_index()
            data = [data,station_data[station][1]]
            event_data.append([station,data])
        except:
            print('\nNão foram encontrados dados no posto %s para o período solicitado.\n'%(station))
    return OrderedDict(event_data)

1
#Preenche falhas nos dados utilizando interpolação linear
#Deve-se definir o percentual aceitável para preencher de falhas

def ask_continue(prompt = 'Entre com Y para continuar e N para interromper o preenchimento das falhas' ):
    try:
        return {'Y':True, 'N': False }[input('Continuar Y/N: ').upper()]
    except KeyError:
        print("Não seja rude e responda apenas com apenas as duas alternativas indicadas.")
        print(prompt)
        ask_continue()

def fill_gap(station_data, gaps_limit = '5'):
    print("\n----Preenchimento de Falhas-----\n")
    filldata=[]
    gaps_limit = int(gaps_limit)/100
    for station in station_data.keys():
        percent_gaps = station_data[station][0]['Data'].isnull().value_counts(True).get(True,0)

        if percent_gaps <= gaps_limit:
            data = station_data[station][0].interpolate()
            data = [data,station_data[station][1]]
            filldata.append([station, data])
            print('O posto {}-{} possuí um percentual de falhas de: {}%.\n'.format(station,station_data[station][1]['Name'],percent_gaps*100))
        else:
            print('O posto {}-{} possuí um percentual de falhas de:  {}%.\n'.format(station,station_data[station][1]['Name'],percent_gaps*100))
            print("E se encontra fora do limite ajustável definido.\n")
            continu = ask_continue()
            if continu:
                data = station_data[station][0].interpolate()
                data = [data,station_data[station][1]]
                filldata.append([station,data])
            else:
                data = station_data[station][0]
                data = [data,station_data[station][1]]
                filldata.append([station,data])

    return OrderedDict(filldata)


#Função que cálcula o percentual de contribuição lateral entre os postos
def del_volume(upstream,downstream):
    vi = upstream['Data'].dropna().sum()
    vo = downstream['Data'].dropna().sum()
    return float((vo - vi) / vi)*100

#Prepara os dados do trecho de análise para entrar na função que simula o método de propagação
def get_stretch_data(station_data, stretch_input = None):
    print("\n----Definição do trecho de análise-----\n")
    if stretch_input:
        upstream = station_data[stretch_input[0]]
        downstream = station_data[stretch_input[1]]
    else:
        indice = 0
        print("Postos:")
        for station in station_data.keys():
            indice+=1
            print ('{}: {} - {}'.format(indice, station, station_data[station][1]['Name']))
        print('\n')
        upstream = station_data[list(station_data.keys())[int(input('Índice do posto à montante do trecho: ')) - 1]]
        downstream = station_data[list(station_data.keys())[int(input('Índice do posto à jusante do trecho: ')) - 1]]
    

    print("\n O trecho definido tem à montante o posto {} e à jusante o posto {}.".format(upstream[1]['Name'], downstream[1]['Name']))
    print('Trecho definido.\n')

    return OrderedDict([['upstream',upstream],['downstream',downstream],['PILinear',del_volume(upstream[0],downstream[0])]])


if __name__ == '__main__':

    file_path = 'C:/Users/cayoh/Google Drive/Graduação/10ºP/ICD/Tarefas/django-db/Django-ORM-master/DadosDeEntrada/PCDS.txt'
    data_path =  'C:/Users/cayoh/Google Drive/Graduação/10ºP/ICD/Tarefas/django-db/Django-ORM-master/DadosDeEntrada'
    cc= 'C:/Users/cayoh/Google Drive/Graduação/10ºP/ICD/Tarefas/django-db/Django-ORM-master/DadosDeEntrada/CurvaChave.txt'

    data = gd.data_read_from_txt(file_station = file_path, DATA_DIR = data_path, f = '0.25H')
    event = get_data_event(data, period = ['10-05-2017','15-05-2017'])
    fill =  fill_gap(event, gaps_limit = '5')
    chave = sdc.curva_chave(fill,cc)
    stretch = get_stretch_data(chave)
    
