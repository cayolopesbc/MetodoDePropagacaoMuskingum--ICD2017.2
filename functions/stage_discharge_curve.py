import pandas as pd
import os
import sys
from collections import OrderedDict
import numpy as np


def coef_from_txt(stage_data,filename):
    stations_coef={}
    try:
        with open(filename) as file:
            for station in stage_data.keys():
                for line in file.readlines():
                    line = line.split()
                    if len(line)==5:
                        station,a,b,h,unit = line
                    else:
                        station = line[0]
                        print("Os coeficientes do %s estão incompletos.\n"%(station))
                        coef = input( 'Inserir manualmente [M] ou Cancelar [C]: ')

                        if coef.upper() == 'M':
                            a = float(input("Inserir valos de alpha: "))
                            b = float(input("Inserir valos de beta: "))
                            h = float(input("Inserir valor ho:"))
                            unit = input("Unidade de ho Metros[M] ou Centímetros[C]: ")
                        else:
                                return print("A rotina foi cancelada. ")
                                
                    station_coef = {'alpha':float(a),'beta': float(b), 'ho':float(h),'Unidade':unit}
                    stations_coef[station] = station_coef 
    except:
        print('Não foi indicado um arquivo. \nNão seja rude.')
        return print("A rotina foi cancelada. ")     
    return stations_coef
        

#Função que faz a conversão cota x vazão
def curva_chave(stage_data,filename = None):
    print("\n----Vazões a partir  da Curva-Chave-----")
    stations_coef = coef_from_txt(stage_data,filename = filename)
    station_flow = []
    for station in stage_data.keys():
        a = stations_coef[station]['alpha']
        b = stations_coef[station]['beta']
        h = stations_coef[station]['ho']
        unit = stations_coef[station]['Unidade']
        if unit.upper() == 'M':
            data = [a*(x/100 - h)**b for x in stage_data[station][0]['Data']]
        else:
            data = [a*(x - h)**b for x in stage_data[station][0]['Data']]

        data = pd.DataFrame(data,columns = ['Data'])
        data['Dates'] = stage_data[station][0]['Dates']
        data = [data,stage_data[station][1]]
        station_flow.append([station,data])

    return OrderedDict(station_flow)

