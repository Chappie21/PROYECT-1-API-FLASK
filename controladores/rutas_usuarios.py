#ESTE ARCHIVO CONTENDRÁ TODAS LAS RUTAS REFERENTES AL USUARIO#

import flask
from modelos import BD, Usuario
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

usuario = flask.Blueprint('usuario', __name__)

##########################################################RUTAS DE USUARIO################################################

#RUTA DE REGISTRO#
@usuario.route('/Usuario/Registro', methods = ['POST'])
def usuario_Registro():
   
   #SE REGISTRA EL NUEVO USUARIO, TOMANDO LOS DATOS#
   
   NuevoU = Usuario(nombre = flask.request.json.get('nombre'), 
            apellido = flask.request.json.get('apellido'),
            email = flask.request.json.get('email'),
            clave = flask.request.json.get('clave'))

   BD.session.add(NuevoU)
   BD.session.commit()
   
   return flask.jsonify({"mensaje":"Usuario creado con éxito"}), 200


#RUTA DE AUTENTICACIÓN#

@usuario.route('/Usuario/InicioSesion', methods = ['POST'])
def usuario_InicioSesion():
    
    #IDENTIFICAR CREDENCIALES#
    Usuario_Sesion = Usuario.query.filter_by( email = flask.request.json.get('email')).first()
   
    if Usuario_Sesion is not None and Usuario_Sesion.Verificar(flask.request.json.get('clave')):
        #SE CREA EL TOKEN#
        access_token = create_access_token(identity=flask.request.json.get('email'))
        return flask.jsonify(access_token = access_token)
    else:
        flask.jsonify({"mensaje":"Error al iniciar sesión. El Email o Clave no son válidos."}) 
        

#RUTA DE VISUALIZACIÓN DE PERFÍL#

@jwt_required()
@usuario.route('/Usuario/VerPerfil', methods = ['GET'])
def usuario_VerPerfil():
    return ""

#RUTA DE EDICIÓN DE USUARIO#

#RUTA DE EDICIÓN DE CONTRASEÑA"

#RUTA DE ELIMINACIÓN DE USUARIO#


