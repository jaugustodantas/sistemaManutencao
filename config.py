SECRET_KEY='teste'

SQLALCHEMY_DATABASE_URI = \
        '{SGBD}://{USUARIO}:{SENHA}@{SERVIDOR}/{database}'.format(
            SGBD = 'mysql+mysqlconnector',
            USUARIO = 'root',
            SENHA = 'teste',
            SERVIDOR ='localhost',
            database = 'manutencaodb'
        )