 #EN ESTE ARCHIVO SE DEFINE EL MODELO PARA LOS USUARIOS CON EL USO DEL ORM SQLALCHEMY PARA BD RELACIONALES#

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

BD = SQLAlchemy()

#ESQUEMA DE USUARIOS#

class Usuario(BD.Model):
    
    #NOMBRE DE LA TABLA#
    __tablename__ = "usuarios"
    
    #ATRIBUTOS#
    
    id = BD.Column(BD.Integer, primary_key = True)
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