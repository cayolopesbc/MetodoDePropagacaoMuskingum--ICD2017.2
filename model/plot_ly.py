import plotly.plotly as py
from plotly.offline import plot,iplot
import plotly.graph_objs as go
from datetime import datetime

def plotmodel_py(modelname,Qin,Qout,Qobs,upstream_code,dowstream_code, period):
    
    mont = 'PCD - {}'.format(upstream_code)
    obs = 'PCD - {}'.format(dowstream_code)
    model ='Modelo {}: PCD - {}'.format(modelname,dowstream_code)
    
    plot_name = [mont, obs,model]
    plot_q = [Qin, Qobs, Qout]
    plot_color = ['rgba(50, 50, 50, .8)', 'rgba(255, 143, 43, .8)','rgba(67, 142, 193, .8)']
    graphics = []
    
    for name in plot_name:
        graph = go.Scatter(
                        x = period,
                        y = plot_q[plot_name.index(name)],
                        mode = 'markers',
                        name = name,
                        marker = dict(
                                    color = plot_color[plot_name.index(name)],
                                    size=3
                                    )
                            )
        graphics.append(graph)

    tt = 'Trecho: {} / {}'.format(upstream_code, dowstream_code)

    layout = go.Layout(title = tt,
                       hovermode ='closest',
                       xaxis = dict(title ='t(horas)',ticklen = 1),
                       yaxis = dict(title = 'Q(m³/s)',ticklen = 1)
                       )
    
    figure = go.Figure(data = graphics, layout = layout)
    now = datetime.now()
    now = str(now.hour) + str(now.minute)+str(now.second)
    filename = modelname + '_'+now+'.html'
    plot_url = iplot(figure, filename = filename)
    #plot_url = iplot(figure, filename = filename, auto_open = True)
#plot_url.replace("\\","//")
    return
