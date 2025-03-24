from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel


class Usuario(Resource):
    def get(self,id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        try:
            return usuario.to_json()
        except:
            return 'Recurso no encontrado', 404

    def put(self,id):
        usuario=db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data: #seteamos con un for recorriendo todos los productos json segun su key y su valor
            setattr(usuario, key, value)
        try:
            db.session.add(usuario)
            db.session.commit()
            return usuario.to_json(), 201
        except:
            return '',404
        
    def delete(self,id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        try:
            db.session.delete(usuario)
            db.session.commit()
            return '',204
        except:
            return '',404
            

class Usuarios(Resource):
    
    def get(self):
        page = 1
        per_page = 5
        usuarios = db.session.query(UsuarioModel)
        
        if request.get_json(silent=True): #Silent = True para ignorar que no recibimos json
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                elif key == 'per_page':
                    per_page = int(value)
       
        usuarios = usuarios.paginate(page=page, per_page=per_page,error_out=True,max_per_page= 10)
        
        return jsonify({
            'usuarios': [usuario.to_json() for usuario in usuarios.items],
            'total': usuarios.total,
            'pages': usuarios.pages,
            'page': page
        })


    def post(self):
         usuario = UsuarioModel.from_json(request.get_json())
         db.session.add(usuario)
         db.session.commit()
         return usuario.to_json(), 201