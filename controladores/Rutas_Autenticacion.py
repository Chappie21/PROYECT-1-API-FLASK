#ESTE ARCHIVO DEFINE TODAS LAS RUTAS RELACIONADAS CON EL USUARIO#

from flask import request, jsonify, Blueprint
from modelos.Modelo_Usuarios import ModeloUsuario
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

RutasDeUsuario = Blueprint('RutasDeAutenticacion', __name__)

#INICIO SE SESIÓN#
@RutasDeUsuario.route('/autenticacion', methods = ['POST'])
def InicioSesion():
    
    #RECEPCIÓN DE DATOS#
    Datos = request.json
    emailU = Datos['email']
    claveU = Datos['clave']
    
    #VALIDACIÓN DE USUARIO E INFORMACIÓN#
    
    Usuario_Sesion = ModeloUsuario.objects(email = emailU).first()
    if Usuario_Sesion is not None and ModeloUsuario.Verificar(Usuario_Sesion.clave, claveU):
    
        #SE CREA EL TOKEN DE VALIDACIÓN DE SESIÓN PARA EL USUARIO#
        access_token = create_access_token(identity = Usuario_Sesion.email)
        return jsonify(
            access_token = access_token,
            email = Usuario_Sesion.email,
            nombre = Usuario_Sesion.nombre,
            apellido = Usuario_Sesion.apellido,
            fotoPerfil = Usuario_Sesion.fotoPerfil,
            visibleEmail = Usuario_Sesion.visibleEmail,
            visibleTop = Usuario_Sesion.visibleTop,
            esAdmin = Usuario_Sesion.esAdmin,
            status = "200"
            ), 200
    else:
        return jsonify({"mensaje":"error al iniciar sesión, credenciales incorrectas o no se encuentra registrado", "status":"409"}), 409