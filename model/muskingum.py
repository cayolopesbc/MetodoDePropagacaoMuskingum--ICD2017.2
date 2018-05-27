from .metrics import*
from collections import OrderedDict
from .map_view import*
from .plot_ly import*

# Q = [Qin,Qobs], Mont = 'Mont - Code Station', Jus = 'Jus - Code Station', Period - Series[Date Inicial/Data Final], dt - passo de tempo, K,X, Pilinear

def muskingum(stretch_data, dt, K, X):
    print("\n----Simulação com o Modelo Muskingum-----")
    #Inicialização das variáveis
    modelname = "Modelo_Muskingum"
    coefficients = OrderedDict([('K',K),('X',X)])

    period = stretch_data['upstream'][0]['Dates']
    ups = stretch_data['upstream'][1]['Code']
    dws = stretch_data['downstream'][1]['Code']
    Qin = list(stretch_data['upstream'][0]['Data'])
    Qobs = list(stretch_data['downstream'][0]['Data'])
    nT = len(Qobs)
    Qout = [0 for _ in range(nT)]
    PILinear = int(stretch_data['PILinear'])
    dt = dt*3600

    # Cálculo dos coeficientes C1, C2, C3:
    K = K*3600
    C0 = float((-K*X+dt/2)/(K*(1-X)+dt/2))
    C1 = float((K*X+dt/2)/(K*(1-X)+dt/2))
    C2 = float((K*(1-X)-dt/2)/(K*(1-X)+dt/2))

    #Condições de Aplicabilidade
    l_inf = dt/2*X/60
    l_sup = dt/2*(1-X)/60
    print("\n-----Limites de aplicabilidade para o parâmetro K----\nLimite Inferior: {}\nLimite Superior: {}\n".format(round(l_inf,4),l_sup))
    
    # Cálculo do hidrograma de saída:

    # No primeiro intervalo de tempo considera-se que a vazão de entrada e saída são constantes:
    Qout[0]= Qin[0]*float((99/100+1))
    

    for j in range(nT):
        Qout[j]=(C0 * Qin[j] + C1 * Qin[j-1] + C2 * Qout[j-1])
        
    #Vazão propagada sem o volume de contribuição lateral no trecho: 
    QoutN = Qout
    #print(QoutN)
    # Adicionando a Contribuição lateral:
    Qout = [qout*(99/100+1) for qout in Qout]
    
    #Métricas da simulação:
    Error = erromodule(Qin,Qobs,Qout,QoutN,dt,modelname)

    results = {'Upstream':stretch_data['upstream'][1], 
                'Downstream':stretch_data['downstream'][1], 
                'Plot':plotmodel_py(modelname,Qin,Qout,Qobs,ups,dws,period)
               }
    
    #Plotagem do Resultado:
    #plot_map(results, modelname)
    print('\n')
    return[modelname,Qin,Qout,Qobs,results,Error]
