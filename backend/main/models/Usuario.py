from ..import db
import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):

        id=db.Column(db.Integer, primary_key=True)
        nombre=db.Column(db.String(45),nullable=False)
        apellido=db.Column(db.String(45),nullable=False)
        email=db.Column(db.String(60),nullable=False,unique=True, index=True)
        role=db.Column(db.String(45),nullable=False,default='cliente')
        telefono=db.Column(db.Integer,nullable=False)
        password=db.Column(db.String(100), nullable=False)
        fecha_registro=db.Column(db.DateTime,nullable=False ,default=dt.datetime.now())
        compras = db.relationship('Compra', back_populates='usuario', cascade="all,delete-orphan")

        #Decoradores
        @property
        def plain_password(self): #Encapsulamiento
            raise AttributeError("Password no se puede leer")
        
        @plain_password.setter
        def plain_password(self, password):
            self.password=  generate_password_hash(password)

        
        def validate_pass(self,password):
            return check_password_hash(self.password,password)

        #MÉTODOS

        #Representar el objeto
        def __repr__(self):
            return f'{self.nombre}'
        
        #Convertir a JSON
        def to_json(self):
            usuario_json={
                'id':self.id,
                'nombre':self.nombre,
                'apellido':self.apellido,
                'email': self.email,
                'role':self.role,
                'telefono': self.telefono,
                'fecha': str(self.fecha_registro)
            }
            return usuario_json
        
        #Convertir en objeto py
        @staticmethod
        def from_json(usuario_json):
            id=usuario_json.get('id')
            nombre=usuario_json.get('nombre')
            apellido=usuario_json.get('apellido')
            email=usuario_json.get('email')
            role=usuario_json.get('role')
            telefono=usuario_json.get('telefono')
            password=usuario_json.get('password')
            fecha_registro=usuario_json.get('fecha_registro')

            return Usuario(
                id=id,
                nombre=nombre,
                apellido=apellido,
                email=email,
                telefono=telefono,
                plain_password=password,
                role=role,
                fecha_registro=fecha_registro
            )

