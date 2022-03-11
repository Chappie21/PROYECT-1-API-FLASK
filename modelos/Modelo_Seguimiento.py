#ESTE ARCHIVO DEFINE EL MODELO PARA EL TOP DE PELÍCULAS DEL USUARIO#

from aplicacion import BD
import mongoengine


class ModeloSeguimiento(BD.Document):
    
    usuario = BD.ReferenceField('ModeloUsuario', reverse_delete_rule = mongoengine.CASCADE)
    pelicula = BD.ReferenceField('ModeloPelicula', reverse_delete_rule = mongoengine.CASCADE)