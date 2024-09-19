from flask import render_template,redirect,request,session,url_for,make_response,flash
from models import Usuarios,Tabelaos
from datetime import datetime
from novo import app,db
import csv
from io import StringIO
from definicoes import FormularioAbriOs,FormularioFecharOs
#relacao login ----------------------------------------------------------------------------
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
    return redirect('/login')

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
    nome = request.form["txtNome"]    #coletar a senha do campo de confirmação para garantir que são iguais
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
        usu = Usuarios.query.filter_by(id=idv).first()
        return render_template ('edituser.html', us=usu)
    
@app.route('/editarusuario',methods=['POST',])
def modificarUsuario():
    eemail = request.form["txtEmail"]
    cargo = request.form["grauUsuario"]
    senha = request.form["txtSenha"] #coletar a senha do campo de confirmação para garantir que são iguais
    nome = request.form["txtNome"]
    user_id = request.form["userId"]
    usuarioEditado = Usuarios.query.filter_by(id=user_id).first()
    if usuarioEditado:
        usuarioEditado.nome = nome
        usuarioEditado.email=eemail
        usuarioEditado.cargo = cargo
        usuarioEditado.senha= senha
        db.session.commit()
    return redirect('/listausuario')
#---------------------------------------------------------------------------------------------------
@app.route('/aberturaos')
def aberturanovaos ():
    if testeUsuario():
        form = FormularioAbriOs()
        return render_template('novaos.html',form=form)
    return redirect('/login')

@app.route('/enviaros', methods=['POST',])
def registronovaos():
    formEntrada = FormularioAbriOs(request.form)
    if formEntrada.validate_on_submit():
        usuario=Usuarios.query.filter_by(email=session['username']).first()
        tipomanutencao = request.form["opcoes"]
        setor = formEntrada.setor.data
        datahoraabertura = datetime.now()
        datahoraabertura = datahoraabertura.strftime("%d/%m/%Y %H:%M")
        maquina = formEntrada.nomeMaquina.data
        e = usuario.id
        emissor = e
        nivelurgencia = request.form["opcoesUrgencia"]
        motivourgencia = request.form["txtMotivoUrgencia"]
        tipo = request.form["opcoesManutencao"]
        descricaodoproblema = formEntrada.descricao.data
        novaOs = Tabelaos(tipomanutencao=tipomanutencao,setor=setor,datahoraabertura =datahoraabertura ,maquina=maquina,emissor=emissor,nivelurgencia=nivelurgencia,motivourgencia=motivourgencia,tipo=tipo,descricaodoproblema =descricaodoproblema) 
        db.session.add(novaOs)
        db.session.commit()
        flash('os aberta com sucesso', 'success')
        return redirect('/listaos')
    flash('houve um erro durante a abertura da os revise as informações e tente novamente', 'error')
    return('/listaos')

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
        form = FormularioFecharOs()
        return render_template ('fecharos.html',form=form, os=searchos)

@app.route('/fecharos', methods =["POST",])
def submit_form():
    idOs = request.form["txtIdOs"]
    osFinalizada = Tabelaos.query.get(idOs) 
    formFinalizar = FormularioFecharOs(request.form)
    if formFinalizar.validate_on_submit():
        osFinalizada.descricaoservico= formFinalizar.descricaoDoServico.data
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
        osFinalizada.finalizada = 's'
        a = formFinalizar.inicioManutencao.data
        b = formFinalizar.fimManutencao.data
        if a > b:
            flash('a data de inicio da manutenção não pode ser maior que a data de fim da manuntenção','error')
            return redirect('/listaos')
        a = a.strftime("%d/%m/%Y %H:%M")
        b = b.strftime("%d/%m/%Y %H:%M")
        testesDeVariaveis(a,b)
        osFinalizada.datahorainicio = a
        osFinalizada.datahoraexecucao = b
        osFinalizada.manutentor = formFinalizar.manutentor1.data
        osFinalizada.manutentor2 = formFinalizar.manutentor2.data
        osFinalizada.manutentor3 = formFinalizar.manutentor3.data
        db.session.commit()
        flash('manutenção finalizada com sucesso','success')
        return redirect('/listaos')
    return redirect('/listaos')
#------------------------------------------------export
@app.route('/exportCSV')
def exportarTabela():
    tabelaexp = Tabelaos.query.all()
    si = StringIO()
    cw = csv.writer(si)
    nomeColunas = Tabelaos.__table__.columns.keys()
    cw.writerow(nomeColunas)    
    for os in tabelaexp:
        cw.writerow([
            os.id, os.tipomanutencao, os.setor, os.datahoraabertura, os.maquina,
            os.emissor, os.nivelurgencia, os.motivourgencia, os.tipo,
            os.descricaodoproblema, os.datahoraexecucao, os.descricaoservico,
            os.trocadeitens, os.nomeitem1, os.nomeitem2, os.nomeitem3, os.nomeitem4,
            os.nomeitem5, os.nomeitem6, os.nomeitem7, os.nomeitem8, os.nomeitem9,
            os.nomeitem10, os.nomeitem11, os.nomeitem12, os.nomeitem13, os.nomeitem14,
            os.nomeitem15, os.qtditem1, os.qtditem2, os.qtditem3, os.qtditem4,
            os.qtditem5, os.qtditem6, os.qtditem7, os.qtditem8, os.qtditem9,
            os.qtditem10, os.qtditem11, os.qtditem12, os.qtditem13, os.qtditem14,
            os.qtditem15, os.houveparada, os.manutentor, os.finalizada, os.datahorainicio,
            os.manutentor2,os.manutentor3
        ])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    
    return output



def testesDeVariaveis(a,b):
    print(a)
    print(b)