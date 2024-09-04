from flask import Flask, render_template,redirect,request,session,url_for,make_response
import webbrowser
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import csv
from io import StringIO

app = Flask(__name__)
app.config.from_pyfile('config.py')
db= SQLAlchemy(app)


from views import *    


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000/login')
    app.run(debug=True)
   # app.run()



