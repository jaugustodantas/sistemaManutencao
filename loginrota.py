from models import Usuarios
from flask import render_template,redirect,request,session,Blueprint

login_bp = Blueprint('loginrota',__name__)

def testeUsuario():
    if 'username' not in session or session['username'] == None:
        return False
    return True

@login_bp.route('/autenticar', methods =['POST',])
def autenticador ():
    usuario = Usuarios.query.filter_by(email=request.form['txtUser']).first()
    if usuario:
        if usuario.senha == request.form['txtPswd']:
            session['username'] = request.form['txtUser']
            session['cargo'] = usuario.cargo
            return redirect('/listaos')
    return redirect('/login')

@login_bp.route('/login')
def direcionarparalogin(): 
    return render_template('login.html')

@login_bp.route('/logout')
def realizarlogout():
    session.pop('username',None) 
    return redirect('/login')  