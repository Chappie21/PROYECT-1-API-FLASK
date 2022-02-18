#ESTE ARCHIVO DEFINE EL MODELO PARA LOS USUARIOS DE LA APLICACIÓN#

from werkzeug.security import generate_password_hash, check_password_hash
from aplicacion import BD

#MODELO DE USUARIOS#

class ModeloUsuario(BD.Model):
    
    #NOMBRE DE LA TABLA#
    __tablename__ = "usuarios"
    
    #ATRIBUTOS PARA EL USUARIO#
    
    idUsuario = BD.Column(BD.Integer, primary_key = True)
    nombre = BD.Column(BD.String(60))
    apellido = BD.Column(BD.String(60))
    email = BD.Column(BD.Text, unique = True)
    clave = BD.Column(BD.Text)
    
    #CONSTRUCTOR#
    
    def __init__(self, nombre, apellido, email, clave):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.clave = self.Encriptar(clave)
    
    #ENCRIPTACIÓN DE CONTRASEÑA#
    
    def Encriptar(self, clave):
        return generate_password_hash(clave)
    
    #VERIFICAR CONTRASEÑA#
    
    def Verificar(self, clave):
        return check_password_hash(self.clave, clave)