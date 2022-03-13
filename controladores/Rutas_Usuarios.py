#ESTE ARCHIVO DEFINE TODAS LAS RUTAS RELACIONADAS CON EL USUARIO#

from flask import request, jsonify, Blueprint
from modelos.Modelo_Usuarios import ModeloUsuario
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

RutasDeUsuario = Blueprint('RutasDeUsuario', __name__)


#REGISTRO DE USUARIO#
@RutasDeUsuario.route('/usuario', methods = ['POST'])
def RegistroNUsuario():
    
    #RECEPCIÓN DE DATOS#
    Datos = request.json
    emailU = Datos['email']
    nombreU = Datos['nombre']
    apellidoU = Datos['apellido']
    claveU = Datos['clave']
    
    #VALIDACIÓN DE EXISTENCIA DE USUARIO A CREAR#
    
    Existencia_Usuario = ModeloUsuario.objects(email = emailU).first()
    if Existencia_Usuario:
        return jsonify({'mensaje':'El usuario ya se encuentra registrado', "status":"409"}), 409
    
    #CREACIÓN DE NUEVO USUARIO#
    NuevoUsuario = ModeloUsuario(
        nombre = nombreU,
        apellido = apellidoU,
        email = emailU,
        clave = ModeloUsuario.Encriptar(claveU)
    ).save()
    
    access_token = create_access_token(identity = NuevoUsuario.email)
    
    return jsonify(
        mensaje = "Usuario creado satisfactoriamente",
        access_token = access_token,
        status = "201"
        ), 201

#EDICIÓN DE USUARIO - DATOS BÁSICOS#
@RutasDeUsuario.route('/usuario', methods = ['PUT'])
@jwt_required()
def EdicionUsuario():
    
    #RECEPCIÓN DE DATOS#
    Datos = request.json
    nombreU = Datos['nombre']
    apellidoU = Datos['apellido']
    emailU = Datos['email']
    fotoPerfilU = Datos['fotoPerfil']
    visibleEmailU = Datos['visibleEmail']
    visibleTopU = Datos['visibleTop']
    
    #UBICACIÓN DEL USUARIO#
    Usuario = ModeloUsuario.objects(email = get_jwt_identity()).first()
    
    if Usuario is not None:
        
        Usuario.update(nombre = nombreU, apellido = apellidoU, email = emailU, fotoPerfil = fotoPerfilU, visibleEmail = visibleEmailU, visibleTop = visibleTopU)
        Usuario.reload()
        
        return jsonify(
                mensaje = "Cambios realizados satisfactoriamente",
                nombre = Usuario.nombre,
                apellido = Usuario.apellido,
                email = Usuario.email,
                fotoPerfil = Usuario.fotoPerfil,
                visibleEmail = Usuario.visibleEmail,
                visibleTop = Usuario.visibleTop,
                status = "201"
            ), 201

    else: 
        return jsonify({'mensaje':"Usuario no encontrado", "status":"409"}), 409
    
#EDICIÓN DE CONTRASEÑA DE USUARIO#
@RutasDeUsuario.route('/usuario/edicionClave', methods = ['PUT'])
@jwt_required() 
def EdicionClave():
    
    #RECEPCIÓN DE DATOS#
    Datos = request.json
    claveNueva = Datos['claveNueva']
    claveAntigua = Datos['claveAntigua']
    
    Usuario = ModeloUsuario.objects(email = get_jwt_identity()).first()
    
    if claveNueva and ModeloUsuario.Verificar(Usuario.clave, claveAntigua):
        
        Usuario.update(clave = ModeloUsuario.Encriptar(claveNueva))
        Usuario.reload()
        
        return jsonify(
            mensaje = "Clave cambiada satisfactoriamente",
            status = "201"
        ), 201
    
    else:
        
        return jsonify(
            mensaje = "No se han llenado los campos o la contraseña actual es incorrecta.",
            status = "409"
        ), 409        
    
    
    
    


    
