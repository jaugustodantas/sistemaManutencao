from flask import render_template,redirect,request,session,flash,Blueprint
from models import Usuarios
from loginrota import testeUsuario
from extensoes import db

pessoa_bp = Blueprint('pessoas',__name__)

@pessoa_bp.route('/cadastro')
def cadastrarNovoUsuario ():
    if 'username' not in session or session['username'] == None:
        return redirect('/login')
    if session['cargo'] =='Gestor':
        return render_template('cadastrouser.html')
    else:
        return redirect('/listaos')

@pessoa_bp.route('/cadastrousuario',methods=['POST',])
def registroUsuarioDb ():
    eemail = request.form["txtEmail"]
    cargo = request.form["grauUsuario"]
    senha = request.form["txtSenha"]
    nome = request.form["txtNome"]    #coletar a senha do campo de confirmação para garantir que são iguais
    testeRepetido = Usuarios.query.filter_by(email=eemail).first()
    if testeRepetido:
        flash('Já existe um usuário com esse e-mail cadastrado','error')
        return redirect('/cadastro')
    
    novoUsuario = Usuarios(email=eemail,cargo=cargo,senha=senha,nome=nome)
    db.session.add(novoUsuario)
    db.session.commit()
    return redirect('/listaos')
@pessoa_bp.route('/listausuario')
def enumerausr():
     if testeUsuario():
        listaurs = Usuarios.query.order_by(Usuarios.id)
        return render_template('listadeusuarios.html',listausr=listaurs)
     return redirect('/login')

@pessoa_bp.route('/editarusr/<int:idv>/<int:modo>')
def vizualizar_usr(idv,modo):
    if modo == 1:
        Usuarios.query.filter_by(id=idv).delete()
        db.session.commit()
        return redirect('/listausuario')
    elif modo == 2:
        usu = Usuarios.query.filter_by(id=idv).first()
        return render_template ('edituser.html', us=usu)
    
@pessoa_bp.route('/editarusuario',methods=['POST',])
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