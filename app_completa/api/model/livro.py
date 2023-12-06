from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from datetime import datetime
from typing import Union

from  model import Base


class Livro(Base):
    __tablename__ = 'livro'
    
    lista = Column("pk_lista", ForeignKey("lista.pk_nome", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    nome = Column("pk_livro", String(140), primary_key=True)
    
    autor = Column(String(101), nullable=False)
    
    formato_lido = Column(String(21))
    recomendado = Column(Boolean)
    motivo = Column(String(301))
    
    personagem_fav = Column(String(401))
    melhores_part = Column(String(501))
    
    avaliacao1 = Column(Integer)
    avaliacao2_nome = Column(String(81))
    avaliacao2 = Column(Integer)
    avaliacao3_nome = Column(String(81))
    avaliacao3 = Column(Integer)
    avaliacao4_nome = Column(String(81))
    avaliacao4 = Column(Integer)
    
    data_comeco = Column(DateTime)
    data_fim = Column(DateTime)
    
    resumo = Column(String(2000))
    quotes = Column(String(2000))
    experiencia = Column(String(4000))
    anotacao = Column(String(3000))

    def __init__(self, lista: str, nome:str, autor:str, formato_lido:str,
                 recomendado:bool, motivo: str, personagem_fav:str, melhores_part:str,
                 avaliacao1:Integer, avaliacao2_nome: str, avaliacao2:Integer, avaliacao3_nome: str,
                 avaliacao3:Integer, avaliacao4_nome:str, avaliacao4:Integer, data_comeco:DateTime, 
                 data_fim:DateTime, resumo:str, quotes: str, experiencia:str, anotacao:str):
        """
        Cria um Livro

        Arguments:
            lista: nome da lista em que o livro está.
            nome: nome do livro.
            autor: autor do livro.
            formato_lido: formato no qual o livro foi lido.
            recomendado: se recomenda esse livro.
            motivo: o motivo para (ou não) recomendar o livro.
            personagem_fav: personagem favorito do livro.
            melhores_part: as melhores partes de um livro.
            avaliacao1: avaliação geral do livro.
            avaliacao2_nome: nome da segunda categoria de avaliação.
            avaliacao2: avaliação na segunda categoria.
            avaliacao3_nome: nome da terceira categoria de avaliação.
            avaliacao3: avaliação na terceira categoria.
            avaliacao4_nome: nome da quarta categoria de avaliação.
            avaliacao4: avaliação na quarta categoria.
            data_comeco: data de quando começou a ler o livro.
            data_fim: data de quando terminou de ler o livro.
            descricao: descrição do livro.
            anotacao: anotação do livro.
        """
        self.lista = lista
        self.nome = nome
        self.autor = autor
        self.formato_lido = formato_lido
        self.recomendado = recomendado
        self.motivo = motivo
        self.personagem_fav = personagem_fav
        self.melhores_part = melhores_part
        self.avaliacao1 = avaliacao1
        self.avaliacao2_nome = avaliacao2_nome 
        self.avaliacao2 = avaliacao2
        self.avaliacao3_nome = avaliacao3_nome
        self.avaliacao3 = avaliacao3
        self.avaliacao4_nome = avaliacao4_nome
        self.avaliacao4 = avaliacao4
        self.data_comeco = data_comeco
        self.data_fim = data_fim
        self.resumo = resumo
        self.quotes = quotes
        self.experiencia = experiencia
        self.anotacao = anotacao
