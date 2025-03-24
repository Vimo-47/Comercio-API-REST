from flask import request, Blueprint
from .. import db
from main.models import UsuarioModel
from flask_jwt_extended import create_access_token
from main.auth.decorators import user_identity_lookup
from main.mail.functions import send_mail

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['POST'])
def login():
    #Buscamos al usuario en la db mediante el mail
    usuario = db.session.query(UsuarioModel).filter(UsuarioModel.email == request.get_json().get('email')).first_or_404()

    #Validamos la contraseña de ese usuario
    if usuario.validate_pass(request.get_json().get("password")):
        #Generamos un nuevo token y le pasamos al usuario como identidad de es token
        access_token = create_access_token(identity=usuario)
        #Devolvemos los valores y el token
        data = {
            'id': str(usuario.id),
            'email': usuario.email,
            'access_token': access_token,
            'role': str(usuario.role)
        }
        return data, 200
    else:
        return 'Incorrect password', 401



@auth.route('/register', methods=['POST'])
def register():
    usuario = UsuarioModel.from_json(request.get_json())
    #Filtra la tabla de emails, si ya existe el email al pasarlo a scalar() dara un número y luego lo comparará con None
    #Si scalar() es None significa que no existe ese email
    #None no es None? Falso, Cualquier numero no es None? Verdadero. Si el email existe da True si no existe False
    exits = db.session.query(UsuarioModel).filter(UsuarioModel.email == usuario.email).scalar() is not None
    if exits:
        return 'email duplicado',409
    else:
        try:
            db.session.add(usuario)
            db.session.commit()
            send_mail([usuario.email],'Bienvenido','register', usuario = usuario)
        except Exception as error:
            db.session.rollback()
            return 'error', 409
        return usuario.to_json(),201