#ESTE ARCHIVO DEFINE UNA SERIE DE CONFIGURACIONES ADICIONALES PARA LA APLICACIÓN#

import os

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')

    
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    


