#ESTE ARCHIVO DEFINE LAS RUTAS RELACIONADAS CON EL USUARIO#

import email
from aplicacion import BD
import flask
from modelos.Modelo_Usuarios import ModeloUsuario
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

RutasUsuario = flask.Blueprint('RutasUsuario', __name__)

#PRUEBA#
@RutasUsuario.route('/Usuario/Index', methods = ['GET'])
def Index():
    return flask.jsonify({"mensaje":"Hola, te doy un saludo"})

#RUTAS DE USUARIO#


#REGISTRO DE USUARIO#

@RutasUsuario.route('/Usuario/NuevoUsuario', methods = ['POST'])
def RegistroNUsuario():
    
    #RECEPCIÓN DE DATOS Y AGREGADO DE NUEVO USUARIO A LA BASE DE DATOS#
    
    NuevoUsuario = ModeloUsuario(nombre = flask.request.json.get('nombre'),
        apellido = flask.request.json.get('apellido'),
        email = flask.request.json.get('email'),                         
        clave = flask.request.json.get('clave'))
    
    
    
    BD.session.add(NuevoUsuario)
    BD.session.commit()
    
    return flask.jsonify({"mensaje":"Usuario creado con éxito"}), 200

#AUTENTICACIÓN DE USUARIO#

@RutasUsuario.route('/Usuario/Autenticar', methods = ['POST'])
def Autenticacion():
        
    #VALIDACIÓN DE DATOS Y COMPROBACIÓN EN LA BASE DE DATOS#
    
    Usuario_Sesion = ModeloUsuario.query.filter_by( email = flask.request.json.get('email')).first()
    
    if Usuario_Sesion is not None and Usuario_Sesion.Verificar(flask.request.json.get('clave')):
        
        #SE CREA EL TOKEN CON EL CUAL EL USUARIO SE ENCUENTRA AUTENTICADO Y SU EMAIL SE USA COMO IDENTIDAD#
        access_token = create_access_token(identity=flask.request.json.get('email'))
        return flask.jsonify(access_token = access_token)
    
    else:
        flask.jsonify({"mensaje":"Error al iniciar sesión. El Email o Clave no son válidos."})
        

#VISUALIZACIÓN DE USUARIO#
@RutasUsuario.route('/Usuario/Perfil', methods = ['GET'])
@jwt_required()
def PerfilUsuario():
    
    #SE CONSULTA LA INFORMACIÓN DEL USUARIO AUTENTICADO EN LA BASE DE DATOS Y SE RETORNAN#
    
    DatosUsuario = ModeloUsuario.query.filter_by( email = get_jwt_identity()).first()
    
    nombreU = DatosUsuario.nombre
    apellidoU = DatosUsuario.apellido

    return flask.jsonify({"nombre":nombreU, "apellido":apellidoU, "email": get_jwt_identity()}), 200
    
#EDICIÓN DE DATOS NO SENSIBLES DE USUARIO#

#EDICIÓN DE CLAVE DE USUARIO#

#ELIMINACIÓN DE USUARIO#

#DIOSITO AYUDAME POR FAVOR# 