from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, Boolean
from datetime import datetime
from typing import Union

from  model import Base


class Livro(Base):
    __tablename__ = 'livro'
    
    lista = Column("pk_lista", ForeignKey("lista.pk_nome", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    id = Column("pk_livro", Integer, primary_key=True)
    
    nome = Column(String(140), unique=True, nullable=False)
    autor = Column(String(81), nullable=False)
    imagem = Column(String(2048))
    
    formato_lido = Column(String(21))
    recomendado = Column(Boolean)
    motivo = Column(String(200))
    
    personagem_fav = Column(String(81))
    melhores_part = Column(String(400))
    
    avalicao = Column(Float)
    experiencia = Column(Float)
    
    data_comeco = Column(DateTime)
    data_fim = Column(DateTime)
    
    descricao = Column(String(4000))
    anotacao = Column(String(4000))

    def __init__(self, nome:str, autor:str, imagem_path:str, formato_lido:str,
                 recomendado:bool, motivo: str, personagem_fav:str, melhores_part:str,
                 avaliacao:float, experiencia:float, data_comeco:DateTime, data_fim:DateTime,
                 descricao:str, anotacao:str):
        """
        Cria um Livro

        Arguments:
            nome: nome do livro.
            autor: autor do livro.
            imagem_path: caminho ou URL de acesso a imagem do livro.
            formato_lido: formato no qual o livro foi lido.
            recomendado: se recomenda esse livro.
            motivo: o motivo para (ou não) recomendar o livro.
            personagem_fav: personagem favorito do livro.
            melhores_part: as melhores partes de um livro.
            avaliacao: avaliação do livro.
            experiencia: experienciado libro.
            data_comeco: data de quando começou a ler o livro.
            data_fim: data de quando terminou de ler o livro.
            descricao: descrição do livro.
            anotacao: anotação do livro.
        """
        self.nome = nome
        self.autor = autor
        self.imagem = imagem_path
        self.formato_lido = formato_lido
        self.recomendado = recomendado
        self.motivo = motivo
        self.personagem_fav = personagem_fav
        self.melhores_part = melhores_part
        self.avaliacao = avaliacao
        self.experiencia = experiencia
        self.data_comeco = data_comeco
        self.data_fim = data_fim
        self.descricao = descricao
        self.anotacao = anotacao
