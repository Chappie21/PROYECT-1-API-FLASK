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


    
