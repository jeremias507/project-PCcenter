import sqlalchemy as db
from sqlalchemy.orm import Session
from dominio.modelos import ProductoModel
from dominio.copymodels import ProductoGuardado
from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from dominio.modelos import Base

class ServicioProducto:

    def __init__(self):
        self.engine_productos = db.create_engine('sqlite:///bd/productos.sqlite', echo=True, future=True)
        self.engine_tienda = db.create_engine('sqlite:///bd/tienda.sqlite', echo=True, future=True)
        Base.metadata.create_all(self.engine_productos)
        Base.metadata.create_all(self.engine_tienda)

    def registrar_producto(self, nombre, precio):
        compra = ProductoGuardado(nombre=nombre, precio=precio)
        with Session(self.engine_tienda) as session:
            session.add(compra)
            session.commit()

    def register(self, nombre, precio):
        producto = ProductoModel(nombre=nombre, precio=precio)
        with Session(self.engine_productos) as session:
            session.add(producto)
            session.commit()

    def modificar(self, nombre, precio, producto_id):
        try:
            with Session(self.engine_productos) as session:
                producto = session.query(ProductoModel).filter_by(id=producto_id).one()
                producto.nombre = nombre
                producto.precio = precio
                session.commit()
                print(f"Producto con ID {producto_id} actualizado correctamente.")
                return True
        except NoResultFound:
            print(f"No se encontró ningún producto con ID {producto_id}. No se realizó ninguna modificación.")
            return False
        except Exception as e:
            print(f"Error al actualizar el producto: {e}")
            return False

    def obtener_productos(self) -> List[ProductoModel]:
        with Session(self.engine_productos) as session:
            productos = session.query(ProductoModel).all()
        return productos

    def eliminar(self, producto_id):
        with Session(self.engine_productos) as session:
            producto = session.query(ProductoModel).filter_by(id=producto_id).first()
            if producto:
                try:
                    session.delete(producto)
                    session.commit()
                    print(f"Producto con ID {producto_id} eliminado correctamente.")
                except IntegrityError as e:
                    session.rollback()
                    print(f"No se pudo eliminar el producto con ID {producto_id}. Error: {e}")
            else:
                print(f"No se encontró ningún producto con ID {producto_id}.")

    def eliminar_todos(self):
        with Session(self.engine_productos) as session:
            try:
                session.query(ProductoModel).delete()
                session.commit()
                print("Todos los productos han sido eliminados.")
            except Exception as e:
                session.rollback()
                print(f"No se pudo eliminar todos los productos: {e}")