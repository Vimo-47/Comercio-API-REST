from .. import jwt
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify

def role_required(roles):
     def decorator(function):
         def wrapper(*args,**kwargs):
             #Verifivamos que JWT sea correcto
             verify_jwt_in_request()
             #Obtenemos las peticiones que estan dentro del JWT
             claims = get_jwt()
             #Verifico que el rol sea el permitido
             if claims['sub']['role'] in roles:
                 return function(*args,**kwargs)
             else:
                 return jsonify({'msg':'No tienes permitida la acción'}), 403
         return wrapper
     return decorator



@jwt.user_identity_loader
def user_identity_lookup(usuario):
    return{
        'usuarioID': usuario.id,
        'role': usuario.role
    }

@jwt.additional_claims_loader
def add_claims_to_accedd_token(usuario):
    claims={
        'id': usuario.id,
        'role': usuario.role
    }
