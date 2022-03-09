#ESTE ARCHIVO DEFINE EL MODELO PARA LOS USUARIOS DE LA APLICACIÓN#

from werkzeug.security import generate_password_hash, check_password_hash
from aplicacion import BD
import mongoengine

#MODELO DE USUARIOS#

class ModeloUsuario(BD.Document):
    
    #ATRIBUTOS PARA EL USUARIO#
    
    nombre = BD.StringField(required = True, max_length = 60)
    apellido = BD.StringField(required = True, max_length = 50)
    email = BD.StringField(required = True)
    emailVisible = BD.BooleanField(default = True)
    fotoPerfil = BD.StringField()
    sexo = BD.StringField(max_length = 7)
    sexoVisible = BD.BooleanField(default = True)    
    clave = BD.StringField(required = True)
    topPeliculas = BD.ListField(BD.ReferenceField('ModeloPelicula', reverse_delete_rule = mongoengine.CASCADE))
    topVisible = BD.BooleanField(default = True)
    rol = BD.StringField(max_length = 25)
        
    #ENCRIPTACIÓN DE CONTRASEÑA#
    
    def Encriptar(self, clave):
        return generate_password_hash(clave)
    
    #VERIFICAR CONTRASEÑA#
    
    def Verificar(self, clave):
        return check_password_hash(self.clave, clave)