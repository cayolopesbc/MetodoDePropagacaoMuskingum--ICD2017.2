# Turn off bytecode generation
import sys
sys.dont_write_bytecode = True

# Django specific settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()

#from functions.add_db import*
from functions.add_db import *
from functions.get_data import *
from functions.modify_data import*
from functions.stage_discharge_curve import *
from model.muskingum import*

# Import your models for use in your script
from ICDR.models import *

if __name__ == '__main__':

    file_path = 'C:/Users/cayoh/Google Drive/Graduação/10ºP/ICD/Tarefas/django-db/Django-ORM-master/DadosDeEntrada/PCDS.txt'
    data_path =  'C:/Users/cayoh/Google Drive/Graduação/10ºP/ICD/Tarefas/django-db/Django-ORM-master/DadosDeEntrada'
    cc = 'C:/Users/cayoh/Google Drive/Graduação/10ºP/ICD/Tarefas/django-db/Django-ORM-master/DadosDeEntrada/CurvaChave.txt'
    station_infos = 'C:/Users/cayoh/Google Drive/Graduação/10ºP/ICD/Tarefas/django-db/Django-ORM-master/DadosDeEntrada/est_fluvio.xls'
    #create_station(station_infos,data_path)
    
    data = data_read_from_txt(file_station = file_path, DATA_DIR = data_path, f = '0.25H')
    data = data_read_from_db(file_station = file_path, f = '0.25H')
        
    event = get_data_event(data, period = ['10-05-2017','30-05-2017'])
    fill =  fill_gap(event, gaps_limit = '5')
    chave = curva_chave(fill,cc)
    stretch = get_stretch_data(chave)
    muskingum(stretch, 0.25,8, 0.30)    
