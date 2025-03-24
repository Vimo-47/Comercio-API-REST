from .. import db

class ProductoCompra(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    productoId = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    producto = db.relationship('Producto', back_populates="productoscompras", uselist=False, single_parent=True)
    compraId = db.Column(db.Integer, db.ForeignKey('compra.id'), nullable=False)
    compra = db.relationship('Compra', back_populates="productoscompras", uselist=False,single_parent=True)


    def __repr__(self):
        return f'id: {self.id}'

    def to_json(self):
        productocompra_json={
            'id': self.id,
            'producto': self.producto.to_json(),
            'compra': self.producto.to_json()
        }
        return productocompra_json

    @staticmethod
    def from_json(productocompra):
        id=productocompra.get('id')
        productoId=productocompra.get('productoId')
        compraId=productocompra.get('compraId')

        return ProductoCompra(
            id=id,
            productoId=productoId,
            compraId=compraId
        )