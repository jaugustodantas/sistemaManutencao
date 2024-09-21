from flask_sqlalchemy import SQLAlchemy
from models import Tabelaos


os = Tabelaos.query.get(15)
usuario = os.id
print(usuario)