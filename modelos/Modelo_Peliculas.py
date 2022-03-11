#ESTE ARCHIVO DEFINE EL MODELO DE LAS PELÍCULAS#

from aplicacion import BD
import mongoengine

class ModeloPelicula(BD.Document):
     
     #ATRIBUTOS PARA LA PELICULA#
     
     nombre = BD.StringField(required = True, unique = True)
     genero = BD.StringField(required = True)
     idioma = BD.StringField(required = True)
     director = BD.StringField(required = True)
     duracion = BD.StringField(required = True)
     fechaEstreno = BD.DateTimeField()
     trailers = BD.ListField(BD.StringField(), default = [])
     imagenes = BD.ListField(BD.StringField(), default = [])
     portada = BD.StringField(default = "")
     descripcion = BD.StringField(default = "")
     calificacion = BD.DecimalField( default = 0 )