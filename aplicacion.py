#APLICACIÓN FLASK#

from datetime import timedelta
import os
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import *

#INSTANCIA Y CONFIGURACIÓN DE LA APLICACIÓN FLASK#

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

load_dotenv()

#CONFIGURACIÓN JWT#

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours = 1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days = 25)
JWT = JWTManager(app)

#CONFIGURACIÓN SQLALCHEMY#

URI = os.getenv('URI_BBDD')
app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
BD = SQLAlchemy(app)

#IMPORTACIÓN Y REGISTRO DE RUTAS MEDIANTE BLUEPRINTS#

from controladores.Usuario import RutasUsuario

app.register_blueprint(RutasUsuario)
 