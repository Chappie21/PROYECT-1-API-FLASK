#APLICACIÓN FLASK#

import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import *

#INSTANCIA Y CONFIGURACIÓN DE LA APLICACIÓN FLASK#

app = Flask(__name__)
app.config.from_object(ConfiguracionDesarrollo)

#CONFIGURACIÓN JWT#

app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
JWT = JWTManager(app)

#CONFIGURACIÓN SQLALCHEMY#
BD = SQLAlchemy(app)

#IMPORTACIÓN Y REGISTRO DE RUTAS MEDIANTE BLUEPRINTS#
#AQUÍ VA A IR EL DONDSDS#
 