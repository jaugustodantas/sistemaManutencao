from extensoes import db

class Tabelaos(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    tipomanutencao = db.Column(db.String(30))
    setor = db.Column(db.String(100))
    datahoraabertura = db.Column(db.String(20))
    maquina = db.Column(db.String(100))
    nivelurgencia = db.Column(db.Text)
    motivourgencia = db.Column(db.Text)
    tipo = db.Column(db.String(30))
    descricaodoproblema = db.Column(db.Text)
    datahoraexecucao = db.Column(db.String(20))
    descricaoservico = db.Column(db.Text)
    trocadeitens = db.Column(db.String(1))
    nomeitem1 = db.Column(db.String(50))
    nomeitem2 = db.Column(db.String(50))
    nomeitem3 = db.Column(db.String(50))
    nomeitem4 = db.Column(db.String(50))
    nomeitem5 = db.Column(db.String(50))
    nomeitem6 = db.Column(db.String(50))
    nomeitem7 = db.Column(db.String(50))
    nomeitem8 = db.Column(db.String(50))
    nomeitem9 = db.Column(db.String(50))
    nomeitem10 = db.Column(db.String(50))
    nomeitem11 = db.Column(db.String(50))
    nomeitem12 = db.Column(db.String(50))
    nomeitem13 = db.Column(db.String(50))
    nomeitem14 = db.Column(db.String(50))
    nomeitem15 = db.Column(db.String(50))
    qtditem1= db.Column(db.Integer)
    qtditem2= db.Column(db.Integer)
    qtditem3= db.Column(db.Integer)
    qtditem4= db.Column(db.Integer)
    qtditem5= db.Column(db.Integer)
    qtditem6= db.Column(db.Integer)
    qtditem7= db.Column(db.Integer)
    qtditem8= db.Column(db.Integer)
    qtditem9= db.Column(db.Integer)
    qtditem10= db.Column(db.Integer)
    qtditem11= db.Column(db.Integer)
    qtditem12= db.Column(db.Integer)
    qtditem13= db.Column(db.Integer)
    qtditem14= db.Column(db.Integer)
    qtditem15= db.Column(db.Integer)
    houveparada = db.Column(db.String(1))
    manutentor = db.Column(db.String(100))
    finalizada = db.Column(db.String(1))
    datahorainicio= db.Column(db.String(20))
    manutentor2 = db.Column(db.String(100))
    manutentor3 = db.Column(db.String(100))
    id_usuario = db.Column(db.Integer,db.ForeignKey("usuarios.id"))

    usuario = db.relationship('Usuarios',backref="ordens_servico",lazy=True)
    def __repr__(self):
        return '<Name %r>' %self.name
    

class Usuarios(db.Model):
    id = db.Column(db.Integer,primary_key= True,autoincrement = True)
    email = db.Column(db.String(50))
    cargo = db.Column(db.String(50))
    senha = db.Column(db.String(50))
    nome = db.Column(db.String(50))
    def __repr__(self):
        return '<Name %r>' %self.name
    
class Estoquemanutencao(db.Model):
    id = db.Column(db.Integer,primary_key= True,autoincrement = True)
    nome_item= db.Column(db.String(50))
    qtd = db.Column(db.Integer)
    codigo = db.Column(db.String(50))
    def __repr__(self):
        return '<Name %r>' %self.name