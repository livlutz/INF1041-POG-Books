from email.mime import base
from sqlalchemy.exc import IntegrityError

from os import urandom

from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI
from flask_cors import CORS
from flask import request, redirect, render_template, flash, session
from model import Usuario, Tracker, Lista, Livro, Session
from logger import logger
from schemas import *

from functools import wraps

info = Info(title="Minha querida API", version="1.0.0")
app = OpenAPI(__name__, info=info)
app.config['SECRET_KEY'] = urandom(12)
CORS(app)

# default
@app.route('/')
def home():
    return redirect('/home')

# wrapper de verificar login
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect('/login')
    return wrap

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
            session['logged_in'] = True
            if 'email' not in session:
                session['email'] = request.form['username_cadastro']
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
                default_list = Lista(request.form['username_cadastro'], 'default')
                try:
                    session.add(new_user)
                    session.add(default_list)
                    session.commit()
                    return redirect('/login')
                except IntegrityError as e:
                    error = "Email já cadastrado"
            else:
                error = 'Senhas diferentes'
        else:
            return redirect('/')
    return render_template('cadastro.html', error=error)

# perfil
@app.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('config_conta.html')

# deslogar
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    return redirect('/login')

# valida login
def validateLogin(email, senha):
    sessionBD = Session()
    query = sessionBD.query(Usuario).filter(Usuario.email == email)
    result = query.first()
    if result:
        if result.senha == senha:
            return True
    return False

# mostra as listas
@app.route('/listas', methods=['GET'])
@login_required
def get_lists():
    sessionBD = Session()
    user = sessionBD.query(Usuario).filter(Usuario.email == session['email']).first()
    listas = sessionBD.query(Lista).filter(Lista.email == user.email)
    return render_template('listas.html', listas = listas)

# abre uma lista
@app.route('/listas/<lista_id>', methods=['GET'])
@login_required
def get_books(lista_id):
    sessionBD = Session()
    user = sessionBD.query(Usuario).filter(Usuario.email == session['email']).first()
    lista = sessionBD.query(Lista).filter(Lista.nome == lista_id and Lista.email == user.email).first()
    if not lista:
        error_msg = "Lista não encontrado na base :/"
        return render_template('error.html', error_code= 404, error_msg=error_msg), 404
    else:
        livros = sessionBD.query(Livro).filter(Livro.lista == lista.nome)
        return render_template('lista.html', livros = livros, lista_id = lista_id)

# abre a tela de registrar livro
@app.route('/listas/<lista_id>/new_book', methods=['GET'])
@login_required
def register_book():
    return render_template('cadastro_livro.html'), 200

# adiciona o livro na lista
@app.route('/listas/<lista_id>/new_book/save', methods=['POST'])
@login_required
def save_book(lista_id):
    sessionBD = Session()
    user = sessionBD.query(Usuario).filter(Usuario.email == session['email']).first()
    lista = sessionBD.query(Lista).filter(Lista.nome == lista_id and Lista.email == user.email).first()
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
                sessionBD.add(livro)
                sessionBD.commit()
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
@app.route('/listas/<lista_id>/<livro_id>', methods=['GET'])
@login_required
def get_livro(lista_id, livro_id):
    sessionBD = Session()
    user = sessionBD.query(Usuario).filter(Usuario.email == session['email']).first()
    lista = sessionBD.query(Lista).filter(Lista.nome == lista_id and Lista.email == user.email).first()
    livro = sessionBD.query(Livro).filter(Livro.lista == lista.nome and Livro.id == livro_id).first()
    if not lista:
        error_msg = "Lista não encontrado na base :/"
        return render_template('error.html', error_code= 404, error_msg=error_msg), 404
    else:
        return render_template('livro.html', livro = livro)

# atualiza livro
@app.route('/listas/<lista_id>/<livro_id>/update', methods=['PUT'])
@login_required
def update_livro(lista_id, livro_id):
    sessionBD = Session()
    # Recupere o produto existente pelo ID
    user = sessionBD.query(Usuario).filter(Usuario.email == session['email']).first()
    lista = sessionBD.query(Lista).filter(Lista.nome == lista_id and Lista.email == user.email).first()
    livro = sessionBD.query(Livro).filter(Livro.id == livro_id and Livro.lista == lista.nome).first()
    if livro is None:
        return render_template("error.html", error_code=404, error_msg="Produto não encontrado :/"), 404
    # Atualize os campos do produto com os dados fornecidos no JSON da solicitação
    livro.nome = request.form['nome_livro']
    livro.autor = request.form['autor_livro']
    livro.formato_lido = request.form['formato_lido']
    livro.recomendado = request.form['recomenda'] == 'sim'
    livro.motivo = request.form['motivo']
    livro.personagem_fav = request.form['personagem_fav']
    livro.melhores_part = request.form['melhores_part']
    livro.avaliacao1 = request.form['avaliacao1']
    livro.avaliacao2_nome = request.form['avaliacao2_nome']
    livro.avaliacao2 = request.form['avaliacao2']
    livro.avaliacao3_nome = request.form['avaliacao3_nome']
    livro.avaliacao3 = request.form['avaliacao3']
    livro.avaliacao4_nome = request.form['avaliacao4_nome']
    livro.avaliacao4 = request.form['avaliacao4']
    livro.data_comeco = request.form['data_comeco']
    livro.data_fim = request.form['data_fim']
    livro.resumo = request.form['resumo']
    livro.quotes = request.form['quotes']
    livro.descricao = request.form['descricao']
    livro.anotacao = request.form['anotacao']
    try:
        # Efetue a atualização do produto
        sessionBD.commit()
        return redirect("/<lista_id>/<livro_id>"), 200
    except IntegrityError as e:
        error_msg = "Erro na atualização do produto :/"
        return render_template("error.html", error_code=409, error_msg=error_msg), 409
    except Exception as e:
        error_msg = "Não foi possível atualizar o produto :/"
        print(str(e))
        return render_template("error.html", error_code=400, error_msg=error_msg), 400

# deletar livro
@app.route('/listas/<lista_id>/<livro_id>/delete', methods=['DELETE'])
@login_required
def delete_livro(lista_id, livro_id):
    sessionBD = Session()
    user = sessionBD.query(Usuario).filter(Usuario.email == session['email']).first()
    lista = sessionBD.query(Lista).filter(Lista.nome == lista_id and Lista.email == user.email).first()
    livro = sessionBD.query(Livro).filter(Livro.lista == lista.nome and Livro.id == livro_id).first()
    count = livro.delete()
    sessionBD.commit()
    if count == 1:
        return redirect('/<lista_id>'), 200
    else: 
        error_msg = "Produto não encontrado na base :/"
        return render_template("error.html", error_code=404, error_msg=error_msg), 404