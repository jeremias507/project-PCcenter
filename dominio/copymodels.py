from sqlalchemy import Column
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ProductoGuardado(Base):
    __tablename__ = "producto_guardado"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150))
    precio = Column(Float)

    def __repr__(self):
        return f'producto_guardado({self.id}, {self.nombre}, {self.precio})'

    def __str__(self):
        return f'producto_guardado({self.id}, {self.nombre}, {self.precio})'

