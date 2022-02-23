#ESTE ARCHIVO DEFINE LAS RUTAS RELACIONADAS CON EL USUARIO#

from aplicacion import BD
import flask
from modelos.Modelo_Usuarios import ModeloUsuario
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

RutasUsuario = flask.Blueprint('RutasUsuario', __name__)

#RUTAS DE USUARIO#


#REGISTRO DE USUARIO#

@RutasUsuario.route('/Usuario/NuevoUsuario', methods = ['POST'])
def RegistroNUsuario():
    
    #VALIDACIÓN DE EXISTENCIA DE USUARIO#
    
    Existencia = ModeloUsuario.query.filter_by( email = flask.request.json.get('email')).first()
    if Existencia:
        return flask.jsonify({"mensaje":"Ya existe un usuario con el correo ingresado. Ingresa uno diferente"}), 409
    
    #RECEPCIÓN DE DATOS Y AGREGADO DE NUEVO USUARIO A LA BASE DE DATOS#
    
    NuevoUsuario = ModeloUsuario(nombre = flask.request.json.get('nombre'),
        apellido = flask.request.json.get('apellido'),
        email = flask.request.json.get('email'),                         
        clave = flask.request.json.get('clave'))
    
    
    BD.session.add(NuevoUsuario)
    BD.session.commit()
    
    return flask.jsonify({"mensaje":"Usuario creado con éxito"}), 201

#AUTENTICACIÓN DE USUARIO#

@RutasUsuario.route('/Usuario/Autenticar', methods = ['POST'])
def Autenticacion():
        
    #VALIDACIÓN DE DATOS Y COMPROBACIÓN EN LA BASE DE DATOS#
    
    Usuario_Sesion = ModeloUsuario.query.filter_by( email = flask.request.json.get('email')).first()
    
    if Usuario_Sesion is not None and Usuario_Sesion.Verificar(flask.request.json.get('clave')):
        
        #SE CREA EL TOKEN CON EL CUAL EL USUARIO SE ENCUENTRA AUTENTICADO Y SU ID SE USA COMO IDENTIDAD#
        access_token = create_access_token(identity = Usuario_Sesion.idUsuario)
        return flask.jsonify(access_token = access_token), 200
    
    #EN CASO DE ALGÚN ERROR#
    return flask.jsonify({"mensaje":"Error al iniciar sesión. El Email o Clave no son válidos."}), 401
        

#VISUALIZACIÓN DE USUARIO#
@RutasUsuario.route('/Usuario/Perfil', methods = ['GET'])
@jwt_required()
def PerfilUsuario():
    
    #SE CONSULTA LA INFORMACIÓN DEL USUARIO AUTENTICADO EN LA BASE DE DATOS Y SE RETORNAN#
    
    DatosUsuario = ModeloUsuario.query.filter_by( idUsuario = get_jwt_identity()).first()
    
    nombreU = DatosUsuario.nombre
    apellidoU = DatosUsuario.apellido
    emailU = DatosUsuario.email

    return flask.jsonify({"nombre":nombreU, "apellido":apellidoU, "email": emailU}), 200
    
#EDICIÓN DE DATOS NO SENSIBLES DE USUARIO#

@RutasUsuario.route('/Usuario/ModificarDatos', methods = ['PUT'])
@jwt_required()
def ModificacionDatosUsuario():
    
    #SE RECOGEN LOS DATOS ENVIADOS PARA LA EDICIÓN DEL USUARIO#
    NuevoEmail = flask.request.json.get('email')
    NuevoNombre = flask.request.json.get('nombre')
    NuevoApellido = flask.request.json.get('apellido')
    
    #VERIFICACIÓN DE LLENADO CORRECTO DE CAMPOS#
    if not NuevoEmail or not NuevoNombre or not NuevoApellido:
        return flask.jsonify({"mensaje":"Por favor rellene correctamente todos los campos."})
    
    #SE REALIZA UNA MODIFICACIÓN A LOS DATOS NO SENSIBLES DEL USUARIO#
    DatosUsuario = ModeloUsuario.query.filter_by( idUsuario = get_jwt_identity()).first()
    
    DatosUsuario.nombre = NuevoNombre
    DatosUsuario.apellido = NuevoApellido
    DatosUsuario.email = NuevoEmail
    
    BD.session.commit()
    
    return flask.jsonify({"mensaje":"Proceso realizado con éxito"}), 200 
    

#EDICIÓN DE CLAVE DE USUARIO#

@RutasUsuario.route('/Usuario/ModificarClave', methods = ['PUT'])
@jwt_required()
def ModificarClaveUsuario():
    
    #TOMAR DATOS ENVIADOS POR EL USUARIO - CLAVE ANTIGUA Y NUEVA CLAVE - #
    
    ClaveAntigua = flask.request.json.get('ViejaClave')
    ClaveNueva = flask.request.json.get('NuevaClave')
    
    #VALIDACIÓN DE CREDENCIAL#
    
    DatosUsuario = ModeloUsuario.query.filter_by( idUsuario = get_jwt_identity()).first()
    
    if ClaveNueva and DatosUsuario.Verificar(ClaveAntigua):
        
        DatosUsuario.clave = DatosUsuario.Encriptar(ClaveNueva)
        BD.session.commit()
        
        return flask.jsonify({"mensaje":"Solicitud realizada satisfactoriamente"}), 200
    
    #EN CASO DE ALGÚN ERROR#
    
    return flask.jsonify({'mensaje':'Error: Error al autenticar. Por favor verifique los datos ingresados.'}), 401

#ELIMINACIÓN DE USUARIO#
@RutasUsuario.route('/Usuario/EliminarUsuario', methods = ['DELETE'])
@jwt_required()
def EliminarUsuario():
    
    #BORRADO DE USUARIO AUTENTICADO#
    
    UsuarioEliminado = ModeloUsuario.query.filter_by( idUsuario = get_jwt_identity()).first()
    
    if not (UsuarioEliminado):
        return flask.jsonify({"mensaje":"Error, el usuario no existe."}), 400
    
    BD.session.delete(UsuarioEliminado)
    BD.session.commit()
    
    return flask.jsonify({"mensaje":"Se ha eliminado su cuenta satisfactoriamente."}), 200

#CERRAR SESIÓN#
@RutasUsuario.route('/Usuario/CerrarSesion', methods = ['DELETE'])
@jwt_required()
def CerrarSesion():
    return flask.jsonify({"mensaje":"Se ha cerrado sesión satisfactoriamente"})

#DIOSITO AYÚDAME POR FAVOR# 