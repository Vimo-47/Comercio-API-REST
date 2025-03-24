from .. import mailsender, db
from flask import current_app, render_template, Blueprint
from flask_mail import Message
from smtplib import SMTPException
from main.models import UsuarioModel, ProductoModel
from main.auth.decorators import role_required


def send_mail(to, subject, template, **kwargs):
    msg = Message(subject, sender=current_app.config['FLASKY_MAIL_SERVER'], recipients=to)
    try:
        msg.body = render_template(f'{template}.txt', **kwargs)
        mailsender.send(msg)
    except SMTPException as error:
        return 'Fallo de email'
    
    return True

mail =Blueprint('mail', __name__, url_prefix='/mail')

@mail.route('/newsletter', methods=['POST'])
@role_required(roles='admin')
def newsletter():
    usuarios = db.session.query(UsuarioModel).filter(UsuarioModel.role == 'cliente').all()
    productos = db.session.query(ProductoModel).all()
    try:
        for usuario in usuarios:
            send_mail([usuario.email], "Productos en Venta", 'newsletter', usuario=usuario, productos = [producto.nombre for producto in productos])

    except SMTPException as error:
        return 'Error en el email'
    return 'Email enviado', 200
