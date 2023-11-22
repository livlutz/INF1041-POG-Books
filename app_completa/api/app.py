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

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if validateLogin(request.form['email'], request.form['password']):
            return redirect('/')
        else:
            error = 'Email ou senha inválidos'
    return render_template('login.html', error=error)

@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    error = None
    if request.method == 'POST':
        if request.form['password'] == request.form['confirm_password']:
            session = Session()
            new_user = Usuario(request.form['email'], request.form['password'])
            try:
                session.add(new_user)
                session.commit()
                return redirect('/login')
            except IntegrityError as e:
                error = "Email já cadastrado"
        else:
            error = 'Senhas diferentes'
    return render_template('cadastro.html', error=error)


def validateLogin(email, senha):
    session = Session()
    query = session.query(Usuario).filter(Usuario.email == email)
    result = query.first()
    if result:
        if result.senha == senha:
            return True
    return False