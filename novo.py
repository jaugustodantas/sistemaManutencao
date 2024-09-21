from flask import Flask
import webbrowser
from extensoes import db
from loginrota import login_bp 
from ordens import ordens_bp
from exportacao import exp_bp
from pessoas import pessoa_bp
from estoque import estoque_bp
app = Flask(__name__)
app.config.from_pyfile('config.py')

db.__init__(app)
app.register_blueprint(login_bp)
app.register_blueprint(ordens_bp)
app.register_blueprint(exp_bp)
app.register_blueprint(pessoa_bp)
app.register_blueprint(estoque_bp)




if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000/login')
    app.run(debug=True)
   # app.run()



