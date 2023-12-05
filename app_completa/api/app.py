from email.mime import base
from sqlalchemy.exc import IntegrityError

from os import urandom

from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI
from flask_cors import CORS
from flask import request, redirect, render_template, flash
from model import Usuario, Tracker, Lista, Livro, Session
from logger import logger
from schemas import *


info = Info(title="Minha querida API", version="1.0.0")
app = OpenAPI(__name__, info=info)
app.config['SECRET_KEY'] = urandom(12)
CORS(app)

# default
@app.route('/')
def home():
    return redirect('/openapi')

# @app.route('/estante')
# def estante():
#     pass

# login
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    print(request.form)
    if request.method == 'POST':
        if request.form['submit'] == 'Cadastrar':
            return redirect('/sign_up')
        if validateLogin(request.form['username_cadastro'], request.form['senha_cadastro']):
            return redirect('/')
        else:
            error = 'Email ou senha inválidos'
            flash(error)
    return render_template('login.html', error=error)

# cadastro
@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    error = None
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
            return redirect('/')
    return render_template('cadastro.html', error=error)

# valida login
def validateLogin(email, senha):
    session = Session()
    query = session.query(Usuario).filter(Usuario.email == email)
    result = query.first()
    if result:
        if result.senha == senha:
            return True
    return False

# abre uma lista
@app.route('/<lista_id>', methods=['GET'])
def get_books(lista_id):
    session = Session()
    lista = session.query(Lista).filter(Lista.nome == lista_id).first()
    if not lista:
        error_msg = "Lista não encontrado na base :/"
        return render_template('error.html', error_code= 404, error_msg=error_msg), 404
    else:
        livros = session.query(Livro).filter(Livro.nome == lista_id)
        return render_template('lista.html', livros = livros, lista_id = lista_id)

# abre a tela de registrar livro
@app.route('/<lista_id>/new_book', methods=['GET'])
def register_book():
    return render_template('cadastro_livro.html'), 200


# adiciona o livro na lista
@app.route('/<lista_id>/new_book/save', methods=['POST'])
def save_book(lista_id):
    session = Session()
    lista = session.query(Lista).filter(Lista.nome == lista_id).first()
    if not lista:
        error_msg = "Lista não encontrado na base :/"
        return render_template('error.html', error_code= 404, error_msg=error_msg), 404
    else:
        if request.form['nome_livro'] and request.form['autor_livro']:
            livro = Livro(
                lista.nome,
                request.form['nome_livro'],
                request.form['autor_livro'],
                request.form['formato_lido'],
                request.form['recomenda'] == 'sim',
                request.form['motivo'],
                request.form['personagem_fav'],
                request.form['melhores_part'],
                request.form['avaliacao1'],
                request.form['avaliacao2_nome'],
                request.form['avaliacao2'],
                request.form['avaliacao3_nome'],
                request.form['avaliacao3'],
                request.form['avaliacao4_nome'],
                request.form['avaliacao4'],
                request.form['data_comeco'],
                request.form['data_fim'],
                request.form['resumo'],
                request.form['quotes'],
                request.form['descricao'],
                request.form['anotacao']
            )
            try:
                session.add(livro)
                session.commit()
                return redirect('/<lista_id>', livro=livro), 200
            except IntegrityError as e:
                error_msg = "Produto de mesmo nome já salvo na base :/"
                return render_template("error.html", error_code=409, error_msg=error_msg), 409
            except Exception as e:
                error_msg = "Não foi possível salvar novo item :/"
                print(str(e))
                return render_template("error.html", error_code=400, error_msg=error_msg), 400
        else:
            error = 'Nome ou autor do livro não preenchidos'
            return redirect('/<lista_id>/new_book', error = error)
        
# visualiza livro
@app.route('/<lista_id>/<livro_id>', methods=['GET'])
def get_livro(lista_id, livro_id):
    session = Session()
    lista = session.query(Lista).filter(Lista.nome == lista_id).first()
    livro = session.query(Livro).filter(Livro.lista == lista_id and Livro.id == livro_id).first()
    if not lista:
        error_msg = "Lista não encontrado na base :/"
        return render_template('error.html', error_code= 404, error_msg=error_msg), 404
    else:
        return render_template('livro.html', livro = livro)


    