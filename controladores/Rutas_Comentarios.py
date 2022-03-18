#ESTE ARCHIVO DEFINE TODAS LAS RUTAS REFERENTES A LOS COMENTARIOS DENTRO DE LA APLICACIÓN#

from flask import request, jsonify, Blueprint
from modelos.Modelo_Usuarios import ModeloUsuario
from modelos.Modelo_Peliculas import ModeloPelicula
from modelos.Modelo_Comentario import ModeloComentario
from modelos.Modelo_Utilidad import ModeloUtilidad
from flask_jwt_extended import jwt_required, get_jwt_identity
from cloudinary import api, uploader
from datetime import datetime
import time

RutasDeComentario = Blueprint('RutasDeComentario', __name__)

# AGREGAR COMENTARIO #
@RutasDeComentario.route('/comentario/<string:idPelicula>', methods = ['POST'])
@jwt_required()
def AgregarComentario(idPelicula):
    
    # RECEPCIÓN DE DATOS #
    Datos = request.json
    
    Usuario = ModeloUsuario.objects(email = get_jwt_identity()).first()
    idPelicula = idPelicula

    descripcion = Datos['descripcionComentario']
    calificacion = Datos['calificacionComentario']
    
    # VALIDACIÓN ANTISPAM - AGREGADO PARA COMENTARIOS #
    yaComentado = ModeloComentario.objects(usuario = str(Usuario.id), pelicula = idPelicula).first()
    
    if yaComentado:
        
         return jsonify(mensaje = "Ya ha dado su opinión en la película actual", status = "400")
    
    else:
        
        # SE CREA EL COMENTARIO, Y SE MODIFICA LA CALIFICACIÓN GENERAL DE LA PELÍCULA COMENTADA #
        
        Pelicula = ModeloPelicula.objects(id = idPelicula).first()
        
        Comentario = ModeloComentario(
            usuario = str(Usuario.id), 
            pelicula = str(Pelicula.id),
            descripcion = descripcion,
            calificacion = calificacion
            ).save()
        
        calificacionTotal = ModeloComentario.objects(pelicula = str(Pelicula.id)).average('calificacion')
        
        Pelicula.update(calificacion = calificacionTotal)
        Pelicula.reload()
    
        return jsonify(mensaje = "Comentario agregado satisfactoriamente.", status = 200), 200
        
        
        
    
    
     
    
    
    
    return ""


    