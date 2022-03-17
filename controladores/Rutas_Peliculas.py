#EN ESTE ARCHIVO DEFINE TODAS LAS RUTAS REFERENTES A LAS PELÍCULAS#

from flask import request, jsonify, Blueprint
from modelos.Modelo_Usuarios import ModeloUsuario
from modelos.Modelo_Peliculas import ModeloPelicula
from flask_jwt_extended import jwt_required
from cloudinary import api, uploader
from datetime import datetime
import time

RutasDePelicula = Blueprint('RutasDePelicula', __name__)

# AGREGAR NUEVA PELÍCULA #
@RutasDePelicula.route('/peliculas', methods = ['POST'])
#@jwt_required()
def RegistroPelicula():
    
    Datos = request.form
    
    # VALIDACIÓN DE DATOS #
    if not Datos:
         
        return jsonify(mensaje = "No se han ingresado datos.", status = "400"), 400
        
    # VERIFICACIÓN DE EXISTENCIA #
    Existencia = ModeloPelicula.objects( nombre = Datos['nombrePelicula']).first()
    if Existencia:
        
        return jsonify(mensaje = "La película ya se encuentra agregada.", status = "400"), 400
    
    # RECEPCIÓN DE DATOS Y AGREGADO DE PELÍCULA #
    
    nombrePelicula = Datos['nombrePelicula']
    generoPelicula = Datos['generoPelicula']
    idiomaPelicula = Datos['idiomaPelicula']
    directorPelicula = Datos['directorPelicula']
    duracionPelicula = Datos['duracionPelicula']
    descripcionPelicula = Datos['descripcionPelicula']
    trailersPelicula = [Datos['trailerPelicula1'], Datos['trailerPelicula2'], Datos['trailerPelicula3']]
    estrenoPelicula = datetime.strptime(Datos['estrenoPelicula'], '%d/%m/%Y')
    
    Pelicula = ModeloPelicula(
       nombre = nombrePelicula, genero = generoPelicula, 
       idioma = idiomaPelicula, director = directorPelicula, 
       duracion = duracionPelicula, descripcion = descripcionPelicula,
       fechaEstreno = estrenoPelicula).save()
    
    portada = request.files['portadaPelicula']
    
    if portada:
        subidaPortada = uploader.upload(portada, folder = f'Pelitacos/{str(Pelicula.id)}', public_id = 'portadaPelicula')
        Pelicula.update(portada = subidaPortada['url'])
        Pelicula.reload()
    
    if trailersPelicula:
        Pelicula.update(trailers = trailersPelicula)
        Pelicula.reload()
    
    if 'imagenes' in request.files:
        url_imagenes = []
        
        for index, imagen in enumerate(request.files.getlist('imagenes'), start = 1):
            print(index, imagen.filename)
            imagenesSubida = uploader.upload(imagen, folder = f'Pelitacos/{str(Pelicula.id)}', public_key = str(time.time()))
            url_imagenes.append(imagenesSubida['url']) 
                
        Pelicula.update(imagenes = url_imagenes)
        Pelicula.reload()
             
    return jsonify(
        mensaje ="Película agregada satisfactoriamente.",
        status = "200",
        idPelicula = str(Pelicula.id),
        nombrePelicula = Pelicula.nombre,
        generoPelicula = Pelicula.genero,
        idiomaPelicula = Pelicula.idioma,
        directorPelicula = Pelicula.director,
        duracionPelicula = Pelicula.duracion,
        estrenoPelicula = Pelicula.fechaEstreno,
        portadaPelicula = Pelicula.portada,
        descripcionPelicula = Pelicula.descripcion,
    ), 200


# TABLÓN DE INICIO #
@RutasDePelicula.route('/inicio', methods = ['GET'])
#@jwt_required()
def MostrarPeliculas():
    # SE OBTIENEN LOS DATOS DE TODAS LAS PELÍCULAS A MOSTRAR EN EL TABLÓN DE INICIO #
    try:
        
        Peliculas = []
        
        for pelicula in ModeloPelicula.objects().order_by('-fechaEstreno'):
            
            Peliculas.append({
                'idPelicula': str(pelicula.id),
                'nombre': pelicula.nombre,
                'genero': pelicula.genero,
                'calificacion': pelicula.calificacion,
                'portada': pelicula.portada,
                'estreno': pelicula.fechaEstreno
                })
        
        return jsonify( mensaje = "Datos obtenidos satisfactoriamente.", datos = Peliculas, status = 200 ), 200
    
    except:    
        
        return jsonify(mensaje = "Error al recibir los datos de las películas.", status = "400"), 400
    
    #portadas = []
            #if pelicula.portada is not None:
             #   portadaPelicula = pelicula.portada
              #  portadas.append(portadaPelicula)