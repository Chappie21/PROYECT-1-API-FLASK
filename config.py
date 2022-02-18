#ESTE ARCHIVO DEFINE UNA SERIE DE CONFIGURACIONES ADICIONALES PARA LA APLICACIÓN#

import os

class Config(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class ConfiguracionDesarrollo(Config):
    DEVELOPMENT = True
    DEBUG = True
    
class ConfiguracionProduccion(Config):
    DEBUG = False
    


