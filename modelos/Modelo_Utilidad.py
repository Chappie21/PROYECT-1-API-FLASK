#ESTE ARCHIVO DEFINE EL MODELO DE UTILIDAD#

from aplicacion import BD
import mongoengine

class ModeloUtilidad(BD.Document):
    
    usuario = BD.ReferenceField('ModeloUsuario', reverse_delete_rule = mongoengine.CASCADE)
    comentario = BD.ReferenceField('ModeloComentario', reverse_delete_rule = mongoengine.CASCADE)