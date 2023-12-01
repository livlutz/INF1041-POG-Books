from sqlalchemy import Column, String
from sqlalchemy_utils import EmailType

from  model import Base


class Usuario(Base):
    __tablename__ = 'usuario'

    email = Column("pk_usuario", EmailType, primary_key=True)
    senha = Column(String(50), nullable=False)

    def __init__(self, email: str, senha: str):
        """
        Cria um Usuario.

        Arguments:
            email {str}: Email do usuario.
            senha {str}: Senha do usuario.
        """
        self.email = email
        self.senha = senha
