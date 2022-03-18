#ESTE ARCHIVO DEFINE EL MODELO DE LOS COMENTARIOS#

from aplicacion import BD
import mongoengine
import datetime


class ModeloComentario(BD.Document):
    
    #ATRIBUTOS DEL COMENTARIO#
    
    usuario = BD.ReferenceField('ModeloUsuario', required = True, reverse_delete_rule = mongoengine.CASCADE)
    pelicula = BD.ReferenceField('ModeloPelicula', required = True, reverse_delete_rule = mongoengine.CASCADE)
    descripcion = BD.StringField(required = True)
    fecha = BD.DateTimeField(default = datetime.datetime.now())
    calificacion = BD.DecimalField( default = 0 )