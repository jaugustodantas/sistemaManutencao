from loginrota import testeUsuario
from definicoes import FomularioEstoque
from models import Estoquemanutencao
from flask import render_template,redirect,request,flash,Blueprint
from extensoes import db    
estoque_bp = Blueprint("estoque",__name__)

@estoque_bp.route('/listaestoque')
def enumerarestoque():
    if testeUsuario():
        listaitem = Estoquemanutencao.query.order_by(Estoquemanutencao.id)
        return render_template('listadeestoque.html',itens=listaitem)

@estoque_bp.route('/cadastaritem')
def cadastroItem():
    if testeUsuario():
        form = FomularioEstoque()
        return render_template('cadastroitem.html',form=form)
    
@estoque_bp.route('/envioitem',methods=["POST",])
def enviarNovoItem():
    formEnvio = FomularioEstoque(request.form)
    nome = formEnvio.nomeDoItem.data
    qtd = formEnvio.quantidade.data
    codigo = formEnvio.codigoDoItem.data
    novoItem = Estoquemanutencao(nome_item=nome,qtd=qtd,codigo=codigo)
    db.session.add(novoItem)
    db.session.commit()
    flash('Item cadastrado com sucesso','success')
    return redirect('/listaos')