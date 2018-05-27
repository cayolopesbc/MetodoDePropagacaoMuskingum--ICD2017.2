import numpy as np
from collections import OrderedDict

def errordata(Qobs,Qout):
    Qobs=np.array(Qobs)
    Qout=np.array(Qout)
    return Qobs,Qout

def filter_nan(s, o):
    #data = np.array([s, o])
    data = np.array([s.flatten(), o.flatten()])
    data = np.transpose(data)
    data = data[~np.isnan(data).any(1)]
    return data[:, 0], data[:, 1]


def NS(Qobs, Qout):
    """Nash Sutcliffe efficiency coefficient"""
    o, s = errordata(Qobs, Qout)
    s, o = filter_nan(s, o)
    return np.round(1 - sum((s - o) ** 2) / sum((o - np.mean(o)) ** 2),3)

def correlation(Qobs, Qout):
    """ correlation coefficient """
    o, s = errordata(Qobs, Qout)
    s, o = filter_nan(s, o)
    if s.size == 0:
        corr = np.NaN
    else:
        corr = np.corrcoef(o, s)[0, 1]
    return corr

def volerrorobs(Qobs,Qout):
    "Error Volume em Relação ao Observado"
    o, s = errordata(Qobs, Qout)
    return (s.sum()-o.sum())/(o.sum())*100

def volerrorin(Qin,QoutN):
    "Error Volume em Relação a Montante"
    o, s = errordata(Qin, QoutN)
    return (s.sum()-o.sum())/(o.sum())*100

def dischargepeakerror(Qobs,Qout):
    "Error Discharge Peak"
    o=max(Qobs)
    s=max(Qout)
    return 100*(s-o)/(o)

def peaktimeerror(Qobs,Qout,dt):
    "Peak Time Error"
    o = Qobs.index(max(Qobs))
    tpo=o*dt #peak time observed in hours
    s = Qout.index(max(Qout))
    tps=s*dt #peak time simulated in hours
    return(tps-tpo)/tpo*100

def allerrors(Qin,Qobs,Qout,QoutN,dt):
    Error =[]
    Error.append(['Corr', correlation(Qobs, Qout)])
    Error.append(['NashSut', NS(Qobs, Qout)])
    Error.append(['VEO', volerrorobs(Qobs, Qout)])
    Error.append(['VEM', volerrorin(Qin,QoutN)])
    Error.append(['PDE', dischargepeakerror(Qobs, Qout)])
    Error.append(['PTE', peaktimeerror(Qobs, Qout, dt)])
    return OrderedDict(Error)

def erromodule(Qin,Qobs,Qout,QoutN,dt,modelname):

    errorindex = {'Corr': 'Coeficiente de Correlação', 'NashSut': 'Coeficiente de Nash-Sutcliffe',
                  'VEO': 'Erro de Volume - OBS(VEO%)', 'VEM': 'Erro de Volume - Montante (VEM%)','PDE': "Erro de Vazão de Pico (PDE%)",
                  'PTE': "Erro de Tempo de Pico (EPT%)"}
    
    ercoef=list(errorindex.keys())
    Error = allerrors(Qin,Qobs,Qout,QoutN,dt)

    #Impressão dos resultados das métricas:
    print('-------Métricas da simulação-------\n')
    for index in ercoef:
        Error[index] = round(Error[index],4)
        print('{}: {}'.format(errorindex[index],Error[index]))
    print('\n')
    return Error

