import os
from flask import Flask
from dotenv import load_dotenv



#Importo el módulo para crear la api-rest
from flask_restful import Api
api = Api()

#Importo el módulo para conectarme con una base de datos SQL
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#Importo el modulo para trabajar con JsonWebToken jwt
from flask_jwt_extended import JWTManager
jwt=JWTManager()

#Importo el modulo para trabajar con el envio del mail
from flask_mail import  Mail
mailsender=Mail()


#Creo la app
def create_app():

    app = Flask(__name__)

    #Cargar las variables de entorno
    load_dotenv()

    #Config Base de datos
    PATH = os.getenv("DATABASE_PATH")
    DB_NAME = os.getenv("DATABASE_NAME")
    if not os.path.exists(f'{PATH}{DB_NAME}'):
        os.chdir(f'{PATH}')
        file = os.open(f'{DB_NAME}', os.O_CREAT)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.config['SQLALCHEMY_DATABASE_URI']= f'sqlite:///{PATH}{DB_NAME}'
    db.init_app(app)    

    #Definir ruta
    import main.resource as resource
    api.add_resource(resource.ClientesResource, '/clientes')
    api.add_resource(resource.ClienteResource, '/cliente/<id>')
    api.add_resource(resource.UsuariosResource, '/usuarios')
    api.add_resource(resource.UsuarioResource, '/usuario/<id>')
    api.add_resource(resource.ProductosResource, '/productos')
    api.add_resource(resource.ProductoResource, '/producto/<id>')
    api.add_resource(resource.ComprasResource, '/compras')
    api.add_resource(resource.CompraResource, '/compra/<id>')
    api.add_resource(resource.ProductosComprasResource, '/productos-compras')
    api.add_resource(resource.ProductoCompraResource, '/producto-compra/<id>')
    
    
    #Iniciar
    api.init_app(app)

    #Configurar JWT
    app.config['JWT_SECRET_KEY'] =os.getenv("JWT_SECRET_KEY")
    
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    jwt.init_app(app)

    #Blueprints
    from main.auth import routes
    app.register_blueprint(auth.routes.auth)

    from main.mail import functions
    app.register_blueprint(mail.functions.mail)

    #Configurar mail
    app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER')

    mailsender.init_app(app)


    return app

