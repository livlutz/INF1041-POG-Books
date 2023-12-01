from email.mime import base
from sqlalchemy.exc import IntegrityError

from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI
from flask_cors import CORS
from flask import request, redirect, render_template
from model import Usuario, Tracker, Lista, Livro, Session
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

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    print(request.form)
    try:
        if request.method == 'POST':
            if request.form['submit'] == 'Cadastrar':
                return redirect('/sign_up')
            if validateLogin(request.form['username_cadastro'], request.form['senha_cadastro']):
                return redirect('/')
            else:
                error = 'Email ou senha inválidos'
        return render_template('login.html', error=error)
    except Exception as e:
        error_msg = "deu ruim"
        return render_template("error.html", error_code=400, error_msg=error_msg), 400

@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    error = None
    print(request.form)
    if request.method == 'POST':
        if request.form['submit'] == "Confirmar":
            if request.form['senha_cadastro'] == request.form['senha_confirma']:
                session = Session()
                new_user = Usuario(request.form['username_cadastro'], request.form['senha_cadastro'])
                try:
                    session.add(new_user)
                    session.commit()
                    return redirect('/login')
                except IntegrityError as e:
                    error = "Email já cadastrado"
            else:
                error = 'Senhas diferentes'
        else:
            redirect('/')
    return render_template('cadastro.html', error=error)


def validateLogin(email, senha):
    session = Session()
    query = session.query(Usuario).filter(Usuario.email == email)
    result = query.first()
    if result:
        if result.senha == senha:
            return True
    return False