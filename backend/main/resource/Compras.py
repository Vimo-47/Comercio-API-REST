from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from .. import db
from main.models import CompraModel
from main.auth.decorators import role_required

class Compra(Resource):

    @role_required(roles=['admin','cliente'])
    def get(self,id):
        compra = db.session.query(CompraModel).get_or_404(id)
        current_user = get_jwt_identity()
        if current_user['usuarioID'] == compra.id or current_user['role']=='admin':
            try:
                return compra.to_json()
            except:
                return 'Recurso no encontrado', 404
        else:
            return 'No tienes aurorización',401

    @role_required(roles=['admin','cliente'])
    def put(self,id):
        compra=db.session.query(CompraModel).get_or_404(id)
        current_user = get_jwt_identity()
        if current_user['usuarioID'] == compra.id or current_user['role']=='admin':
            data = request.get_json().items()
            for key, value in data: #seteamos con un for recorriendo todos los productos json segun su key y su valor
                setattr(compra, key, value)
            try:
                db.session.add(compra)
                db.session.commit()
                return compra.to_json(), 201
            except:
                return '',404
        else:
            return 'No tienes autorización', 404

    @role_required(roles=['admin','cliente'])        
    def delete(self,id):
        compra = db.session.query(CompraModel).get_or_404(id)
        current_user = get_jwt_identity()
        if current_user['usuarioID'] == compra.id or current_user['role']=='admin':
            try:
                db.session.delete(compra)
                db.session.commit()
                return '',204
            except:
                return '',404
        else:
            return 'No tienes aurorizacion', 401    

class Compras(Resource):
    
    @role_required(roles=['admin'])
    def get(self):
        page = 1
        per_page = 5
        compras = db.session.query(CompraModel)
        
        if request.get_json(silent=True): #Silent = True para ignorar que no recibimos json
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                elif key == 'per_page':
                    per_page = int(value)
       
        compras = compras.paginate(page=page, per_page=per_page,error_out=True,max_per_page= 10)
        
        return jsonify({
            'compras': [compra.to_json() for compra in compras.items],
            'total': compras.total,
            'pages': compras.pages,
            'page': page
        })

    @role_required(roles=['admin', 'cliente'])
    def post(self):
         compra = CompraModel.from_json(request.get_json())
         db.session.add(compra)
         db.session.commit()
         return compra.to_json(), 201