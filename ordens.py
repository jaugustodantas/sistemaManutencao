from extensoes import db
from models import Usuarios, Tabelaos
from flask import render_template,redirect,request,session,flash,Blueprint,url_for
from definicoes import FormularioAbriOs,FormularioFecharOs
from datetime import datetime
from loginrota import testeUsuario

ordens_bp = Blueprint('ordens',__name__)

@ordens_bp.route('/aberturaos')
def aberturanovaos ():
    if testeUsuario():
        form = FormularioAbriOs()
        return render_template('novaos.html',form=form)
    return redirect('/login')

@ordens_bp.route('/enviaros', methods=['POST',])
def registronovaos():
    formEntrada = FormularioAbriOs(request.form)
    if formEntrada.validate_on_submit():
        usuario=Usuarios.query.filter_by(email=session['username']).first()
        tipomanutencao = request.form["opcoes"]
        setor = formEntrada.setor.data
        datahoraabertura = datetime.now()
        datahoraabertura = datahoraabertura.strftime("%d/%m/%Y %H:%M")
        maquina = formEntrada.nomeMaquina.data
        id_usuario = usuario.id
        nivelurgencia = request.form["opcoesUrgencia"]
        motivourgencia = request.form["txtMotivoUrgencia"]
        tipo = request.form["opcoesManutencao"]
        descricaodoproblema = formEntrada.descricao.data
        novaOs = Tabelaos(tipomanutencao=tipomanutencao,setor=setor,datahoraabertura =datahoraabertura ,maquina=maquina,id_usuario=id_usuario,nivelurgencia=nivelurgencia,motivourgencia=motivourgencia,tipo=tipo,descricaodoproblema =descricaodoproblema) 
        db.session.add(novaOs)
        db.session.commit()
        flash('os aberta com sucesso', 'success')
        return redirect('/listaos')
    flash('houve um erro durante a abertura da os revise as informações e tente novamente', 'error')
    return('/listaos')

@ordens_bp.route('/listaos')
def enumeraros():
     if testeUsuario():
        listadeos = Tabelaos.query.filter_by(finalizada = None).order_by(Tabelaos.id)
        return render_template('listadasos.html',itens=listadeos)
     return redirect('/login')

@ordens_bp.route('/vizualizar/<int:idv>/<int:modo>')
def vizualizar_os(idv,modo):
    searchos = Tabelaos.query.filter_by(id=idv).first()
    idbusr = searchos.id_usuario
    usuariosearch = Usuarios.query.filter_by(id=idbusr).first()
    if modo == 1:
        return render_template ('visualizaros.html', os=searchos,usr=usuariosearch)
    elif modo == 2:
        form = FormularioFecharOs()
        return render_template ('fecharos.html',form=form, os=searchos,usr=usuariosearch)

@ordens_bp.route('/fecharos', methods =["POST",])
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
#        testesDeVariaveis(a,b)
        osFinalizada.datahorainicio = a
        osFinalizada.datahoraexecucao = b
        osFinalizada.manutentor = formFinalizar.manutentor1.data
        osFinalizada.manutentor2 = formFinalizar.manutentor2.data
        osFinalizada.manutentor3 = formFinalizar.manutentor3.data
        db.session.commit()
        flash('manutenção finalizada com sucesso','success')
        return redirect('/listaos')
    return redirect('/listaos')

def testando(a):
    print(type(a))
    print(a)
    print('************')