from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Livro(Base):
    __tablename__ = 'livro'
    
    lista = Column("pk_lista", ForeignKey("lista.pk_nome", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    id = Column("pk_livro", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    descricao = Column(String(4000))
    editora = Column(String(400))
    imagem_path = Column(String(2048))
    avalicao = Column(Float)
    categoria = Column(String(200))
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, nome:str, descricao:str, editora:str, avalicao:float,
                 imagem_path:str, categoria: str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Livro

        Arguments:
            nome: nome do livro.
            descricao: descrição do livro.
            editora: qual a editora do livro.
            imagem_path: caminho ou URL de acesso a imagem do livro
            avaliacao: avaliacao do livro
            categoria: identifica a categoria do livro
            data_insercao: data de quando o livro foi inserido à base
        """
        self.nome = nome
        self.descricao = descricao
        self.editora = editora
        self.avalicao = avalicao
        self.imagem_path = imagem_path
        self.categoria = categoria
        if data_insercao:
            self.data_insercao = data_insercao
