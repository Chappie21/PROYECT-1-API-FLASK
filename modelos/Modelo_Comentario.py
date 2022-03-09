#ESTE ARCHIVO DEFINE EL MODELO DE LOS COMENTARIOS#

from aplicacion import BD
import mongoengine

class ModeloComentario(BD.Document):
    
    #ATRIBUTOS DEL COMENTARIO#
    
    usuario = BD.ReferenceField('ModeloUsuario', required = True, reverse_delete_rule = mongoengine.CASCADE)
    pelicula = BD.ReferenceField('ModeloPelicula', required = True, reverse_delete_rule = mongoengine.CASCADE)
    descripcion = BD.StringField(required = True)
    fecha = BD.DateTimeField()
    calificacion = BD.DecimalField( default = 0 )
    utilidad = BD.ListField(BD.ReferenceField('ModeloUtilidad', reverse_delete_rule = mongoengine.CASCADE))