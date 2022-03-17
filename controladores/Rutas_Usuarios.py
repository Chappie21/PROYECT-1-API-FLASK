#ESTE ARCHIVO DEFINE TODAS LAS RUTAS RELACIONADAS CON EL USUARIO#

from flask import request, jsonify, Blueprint
from modelos.Modelo_Usuarios import ModeloUsuario
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from cloudinary import api, uploader

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
        idUsuario = str(NuevoUsuario.id),
        email = NuevoUsuario.email,
        nombre = NuevoUsuario.nombre,
        apellido = NuevoUsuario.apellido,
        fotoPerfil = NuevoUsuario.fotoPerfil,
        visibleEmail = NuevoUsuario.visibleEmail,
        visibleTop = NuevoUsuario.visibleTop,
        esAdmin = NuevoUsuario.esAdmin,
        access_token = access_token,
        status = "201"
        ), 201


#INICIO SE SESIÓN#
@RutasDeUsuario.route('/usuario/autenticar', methods = ['POST'])
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
            idUsuario = str(Usuario_Sesion.id),
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


#EDICIÓN DE USUARIO - DATOS BÁSICOS#
@RutasDeUsuario.route('/usuario', methods = ['PUT'])
@jwt_required()
def EdicionUsuario():
    
    #RECEPCIÓN DE DATOS#
    Datos = request.json
    nombreU = Datos['nombre']
    apellidoU = Datos['apellido']
    emailU = Datos['email']
    
    #UBICACIÓN DEL USUARIO#
    Usuario = ModeloUsuario.objects(email = get_jwt_identity()).first()
    
    if Usuario is not None:
        
        Usuario.update(nombre = nombreU, apellido = apellidoU, email = emailU)
        Usuario.reload()
        
        return jsonify(
                mensaje = "Cambios realizados satisfactoriamente",
                nombre = Usuario.nombre,
                apellido = Usuario.apellido,
                email = Usuario.email,
                status = "201"
            ), 201

    else: 
        return jsonify({'mensaje':"Usuario no encontrado", "status":"409"}), 409
    
    
#EDICIÓN DE FOTO DE PERFIL DE USUARIO#
@RutasDeUsuario.route('/usuario/editarFoto', methods = ['POST'])
@jwt_required()
def EditarFoto_Usuario():
    
    #RECEPCIÓN DE FOTO DE PERFIL Y UBICACIÓN DEL USUARIO#
    
    Usuario = ModeloUsuario.objects(email = get_jwt_identity()).first()
    fotoPerfilU = request.files['archivo']
    
    if fotoPerfilU:
        
        #GUARDADO DE LA FOTO DE PERFIL DEL USUARIO#
        subidaFoto = uploader.upload(fotoPerfilU, folder = f'Pelitacos/{Usuario.id}', public_id = ' fotoPerfil')
        Usuario.update(fotoPerfil = subidaFoto['url'])
        Usuario.reload()
        
        return jsonify(
            mensaje = "Se han guardado los cambios satisfactoriamente.",
            status = "200",
        ), 200
    
    else:
        
        return jsonify(
            mensaje = "No ha seleccionado ningún archivo o el seleccionado no es válido.",
            status = "400"
        ), 400
    
    
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
            status = "201"), 201
    
    else:
        
        return jsonify(
            mensaje = "No se han llenado los campos o la contraseña actual es incorrecta.",
            status = "409"
        ), 409        
    
#VER DATOS DEL USUARIO#
@RutasDeUsuario.route('/usuario', methods = ['GET'])
@jwt_required()
def VerUsuario():
    
    #RECOLECCIÓN DE DATOS DEL USUARIO#
    Usuario = ModeloUsuario.objects( email = get_jwt_identity()).first()
    
    #PELÍCULAS QUE SIGUE EL USUARIO#
    
    #COMENTARIOS MÁS RELEVANTES DEL USUARIO#
    
    return jsonify(
        nombre = Usuario.nombre,
        apellido = Usuario.apellido,
        emailU = Usuario.email,
        fotoPerfil = Usuario.fotoPerfil,
        visibleTop = Usuario.visibleTop,
        visibleEmail = Usuario.visibleEmail,
        status = 200
    ), 200
    
    
#ELIMINACIÓN DE USUARIO#
@RutasDeUsuario.route('/usuario', methods = ['DELETE'])
@jwt_required()
def EliminarUsuario():
    
    #VERFICIACIÓN DEL USUARIO A ELIMINAR#
    Usuario = ModeloUsuario.objects( email = get_jwt_identity()).first()
    if Usuario:
        Usuario.delete()
          
        return jsonify(mensaje = "Se ha eliminado el usuario satisfactoriamente.", status = "200")  
         
    else:
        
        return jsonify(mensaje = "El usuario no existe.",status = "409")