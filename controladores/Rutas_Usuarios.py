#ESTE ARCHIVO DEFINE TODAS LAS RUTAS RELACIONADAS CON EL USUARIO#

from flask import request, jsonify, Blueprint
from modelos.Modelo_Usuarios import ModeloUsuario
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

RutasDeUsuario = Blueprint('RutasDeUsuario', __name__)


#REGISTRO DE USUARIO#
@RutasDeUsuario.route('/Usuario/RegistroUsuario', methods = ['POST'])
def RegistroNUsuario():
    
    #VALIDACIÓN DE EXISTENCIA DE USUARIO A CREAR#
    
    Existencia_Usuario = ModeloUsuario.objects(email = request.json.get('email'))
    if Existencia_Usuario:
        return jsonify({'mensaje':'El usuario ya se encuentra registrado'}), 409
    
    #CREACIÓN DE NUEVO USUARIO#
    NuevoUsuario = ModeloUsuario(
        nombre = request.json.get("nombre"),
        apellido = request.json.get("apellido"),
        email = request.json.get("email"),
        clave = ModeloUsuario.Encriptar(request.json.get("clave"))
    ).save()
    
    return jsonify({"mensaje":"Usuario creado satisfactoriamente"}), 201

#INICIO SE SESIÓN#
@RutasDeUsuario.route('/Usuario/InicioSesion', methods = ['POST'])
def InicioSesion():
    
    #VALIDACIÓN DE USUARIO E INFORMACIÓN#
    
    Usuario_Sesion = ModeloUsuario.objects(email = request.json.get('email')).first()
    if Usuario_Sesion is not None and ModeloUsuario.Verificar(Usuario_Sesion.clave, request.json.get('clave')):
    
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



    
