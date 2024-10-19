import sqlalchemy as db
import dominio.modelos as modelos
import util.generico as gen

nombre_carpeta = "bd"

ruta = "./"

gen.crear_carpeta(ruta, nombre_carpeta)

engine = db.create_engine('sqlite:///bd/tienda.sqlite', echo=True, future=True)

modelos.Base.metadata.create_all(engine)