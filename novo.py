from flask import Flask, render_template,redirect,request,session,url_for
import webbrowser
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key ='TESTE'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    "{SGBD}://{USUARIO}:{SENHA}@{SERVIDOR}/{database}".format(
            SGBD = 'mysql+mysqlconnector',
            USUARIO = 'root',
            SENHA = 'senha',
            SERVIDOR ='localhost',
            database = 'manutencaodb')
db= SQLAlchemy(app)

class Tabelaos(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    tipomanutencao = db.Column(db.String(30))
    setor = db.Column(db.String(100))
    datahoraabertura = db.Column(db.String(20))
    maquina = db.Column(db.String(100))
    emissor = db.Column(db.String(100))
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
    
def testeUsuario():
    if 'username' not in session or session['username'] == None:
        return False
    return True


@app.route('/autenticar', methods =['POST',])
def autenticador ():
    usuario = Usuarios.query.filter_by(email=request.form['txtUser']).first()
    if usuario:
        if usuario.senha == request.form['txtPswd']:
            session['username'] = request.form['txtUser']
            session['cargo'] = usuario.cargo
            return redirect('/listaos')

@app.route('/login')
def direcionarparalogin(): 
    return render_template('login.html')

@app.route('/logout')
def realizarlogout():
    session.pop('username',None) 
    return redirect('/login')       
# ------------------------------------ relacao de usuarios --------------------------------
@app.route('/cadastro')
def cadastrarNovoUsuario ():
    if 'username' not in session or session['username'] == None:
        return redirect('/login')
    if session['cargo'] =='Gestor':
        return render_template('cadastrouser.html')
    else:
        return redirect('/listaos')

@app.route('/cadastrousuario',methods=['POST',])
def registroUsuarioDb ():
    eemail = request.form["txtEmail"]
    cargo = request.form["grauUsuario"]
    senha = request.form["txtSenha"]
    nome = request.form["txtNome"]
    testeRepetido = Usuarios.query.filter_by(email=eemail).first()
    if testeRepetido:
        return render_template('usuariojaexiste.html')
    
    novoUsuario = Usuarios(email=eemail,cargo=cargo,senha=senha,nome=nome)
    db.session.add(novoUsuario)
    db.session.commit()
    return redirect('/listaos')
@app.route('/listausuario')
def enumerausr():
     if testeUsuario():
        listaurs = Usuarios.query.order_by(Usuarios.id)
        return render_template('listadeusuarios.html',listausr=listaurs)
     return redirect('/login')

@app.route('/editarusr/<int:idv>/<int:modo>')
def vizualizar_usr(idv,modo):
    if modo == 1:
        Usuarios.query.filter_by(id=idv).delete()
        db.session.commit()
        return redirect('/listausuario')
    elif modo == 2:
        searchos = Tabelaos.query.filter_by(id=idv).first()
        return render_template ('fecharos.html', os=searchos)

#---------------------------------------------------------------------------------------------------
@app.route('/aberturaos')
def aberturanovaos ():
    if testeUsuario():
        return render_template('novaos.html')
    return redirect('/login')

@app.route('/enviaros', methods=['POST',])
def registronovaos():
    usuario=Usuarios.query.filter_by(email=session['username']).first()
    tipomanutencao = request.form["opcoes"]
    setor = request.form["txtSetor"]
    datahoraabertura = datetime.now()
    datahoraabertura = datahoraabertura.strftime("%d/%m/%Y %H:%M")
    maquina = request.form["txtMaquina"]
    e = usuario.id
    emissor = e
    nivelurgencia = request.form["opcoesUrgencias"]
    motivourgencia = request.form["txtMotivoUrgencia"]
    tipo = request.form["opcoesManutencao"]
    descricaodoproblema = request.form["descricao"]
    novaOs = Tabelaos(tipomanutencao=tipomanutencao,setor=setor,datahoraabertura =datahoraabertura ,maquina=maquina,emissor=emissor,nivelurgencia=nivelurgencia,motivourgencia=motivourgencia,tipo=tipo,descricaodoproblema =descricaodoproblema) 
    db.session.add(novaOs)
    db.session.commit()
    return redirect('/aberturaos')

@app.route('/listaos')
def enumeraros():
     if testeUsuario():
        listadeos = Tabelaos.query.filter_by(finalizada = None).order_by(Tabelaos.id)
        return render_template('listadasos.html',itens=listadeos)
     return redirect('/login')

@app.route('/vizualizar/<int:idv>/<int:modo>')
def vizualizar_os(idv,modo):
    if modo == 1:
        searchos = Tabelaos.query.filter_by(id=idv).first()
        idbusr = searchos.emissor
        usuariosearch = Usuarios.query.filter_by(id=idbusr).first()
        return render_template ('visualizaros.html', os=searchos, usr=usuariosearch)
    elif modo == 2:
        searchos = Tabelaos.query.filter_by(id=idv).first()
        return render_template ('fecharos.html', os=searchos)

@app.route('/fecharos', methods =["POST",])
def submit_form():
    idOs = request.form["txtIdOs"]
    osFinalizada = Tabelaos.query.get(idOs) 
    osFinalizada.datahoraexecucao = request.form["fimManutencao"] 
    osFinalizada.descricaoservico= request.form["descricaoServico"]
    if request.form["houveTroca"] == 'Sim':
        osFinalizada.trocadeitens = 's'
        for i in range(1,16):
            nomepeca = f"nomePeca{i}"
            qtd = f'qtdPeca{i}'
            if request.form[nomepeca]:
                setattr(osFinalizada,f"nomeitem{i}", request.form[nomepeca])
                setattr(osFinalizada,f"qtditem{i}", request.form[qtd])
    else:
        osFinalizada.trocadeitens = 'n'

    if request.form["houveParada"] == "Sim":
        osFinalizada.houveparada= 's'
    else:
        osFinalizada.houveparada= 'n'
    osFinalizada.manutentor = request.form["nomeManutentor"]
    osFinalizada.finalizada = 's'
    osFinalizada.datahorainicio = request.form["inicioManutencao"]
    db.session.commit()
    return redirect('/listaos')

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000/login')
    app.run(debug=True)
   # app.run()



