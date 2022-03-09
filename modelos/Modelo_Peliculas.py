#ESTE ARCHIVO DEFINE EL MODELO DE LAS PELÍCULAS#

from aplicacion import BD
import mongoengine

class ModeloPelicula(BD.Document):
     
     #ATRIBUTOS PARA LA PELICULA#
     
     nombre = BD.StringField(required = True)
     genero = BD.StringField(required = True)
     clasificacion = BD.StringField(required = True)
     idioma = BD.StringField(required = True)
     director = BD.StringField(required = True)
     productor = BD.StringField(required = True)
     duracion = BD.StringField(required = True)
     fechaEstreno = BD.DateTimeField()
     trailers = BD.ListField(BD.StringField())
     imagenes = BD.ListField(BD.StringField())
     portada = BD.StringField()
     calificacion = BD.DecimalField( default = 0 )
     comentarios = BD.ListField(BD.ReferenceField('ModeloComentario', reverse_delete_rule = mongoengine.CASCADE))