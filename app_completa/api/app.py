from email.mime import base
from sqlalchemy.exc import IntegrityError

from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI
from flask_cors import CORS
from flask import request, redirect, render_template
from model import Usuario, Tracker, Lista, Livro
from logger import logger
from schemas import *


info = Info(title="Minha querida API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


@app.route('/')
def home():
    return redirect('/openapi')

@app.route('/estante')
def estante():
    pass

@app.route('/login', methods=['POST'])
def login():
    error = None
    if request.method == 'POST':
        if validateLogin(request.form['username'], request.form['password']):
            return redirect('/')
        else:
            error = 'Email ou senha inválidos'
    return render_template('login.html', error=error)

@app.route('/sign_up', methods=['POST'])
def sign_up():
    error = None
    if request.method == 'POST':
        if request.form['password'] == request.form['confirm_password']:
            if True: # testar se email já tem no banco de dados
                #include in database
                return redirect('/login')
            else:
                error = 'Email já cadastrado'
        else:
            error = 'Senhas diferentes'
    return render_template('cadastro.html', error=error)


def validateLogin(email, senha):
    #acessa bd, acha e verifica
    pass