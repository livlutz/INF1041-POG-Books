from sqlalchemy import Column, Integer, String, Date, ForeignKey
from datetime import date

from  model import Base

class Lista(Base):
    __tablename__ = 'lista'
    
    email = Column("pk_email", ForeignKey("usuario.pk_usuario", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    nome = Column("pk_nome", String(50), nullable=False, primary_key=True)

    def __init__(self, email: str, nome: str):
        """
        Cria um Lista.

        Arguments:
            email {str}: Email do usuario.
            nome {str}: Nome da lista.
        """
        self.email = email
        self.nome = nome