#ESTE ARCHIVO DEFINE EL MODELO PARA LOS USUARIOS DE LA APLICACIÓN#

from werkzeug.security import generate_password_hash, check_password_hash
from aplicacion import BD
import mongoengine

#MODELO DE USUARIOS#

class ModeloUsuario(BD.Document):
    
    #ATRIBUTOS PARA EL USUARIO#
    
    nombre = BD.StringField(required = True, max_length = 60)
    apellido = BD.StringField(required = True, max_length = 50)
    email = BD.StringField(required = True, unique = True)
    visible_Email = BD.BooleanField(default = True)
    fotoPerfil = BD.StringField(default = "")   
    clave = BD.StringField(required = True)
    visible_Top = BD.BooleanField(default = True)
    isAdmin = BD.BooleanField(default = True)
        
    #ENCRIPTACIÓN DE CONTRASEÑA#
    
    def Encriptar(clave):
        return generate_password_hash(clave)
    
    #VERIFICAR CONTRASEÑA#
    
    def Verificar(self, clave):
        return check_password_hash(self.clave, clave)