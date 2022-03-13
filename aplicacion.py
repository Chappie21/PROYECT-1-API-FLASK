#APLICACIÓN FLASK#

from datetime import timedelta
import os
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from config import *

#INSTANCIA Y CONFIGURACIÓN DE LA APLICACIÓN FLASK#

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
load_dotenv()

# Habilitar CORS
cors = CORS(app, supports_credentials = True)

#CONFIGURACIÓN JWT#

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours = 2)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days = 25)
JWT = JWTManager(app)

#CONFIGURACIÓN MONGOENGINE#

app.config['MONGODB_SETTINGS'] = {'host':os.getenv('URI_BBDD'), 'db':'Pelitacos_BD'}
BD = MongoEngine(app)

#IMPORTACIÓN Y REGISTRO DE RUTAS MEDIANTE BLUEPRINTS#

from controladores.Rutas_Usuarios import RutasDeUsuario

app.register_blueprint(RutasDeUsuario) 