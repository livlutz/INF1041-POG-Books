from sqlalchemy import Column, String

from  model import Base


class Usuario(Base):
    __tablename__ = 'usuario'

    email = Column("pk_usuario", String(320), primary_key=True)
    senha = Column(String(40), not_null=True)

    def __init__(self, email: str, senha: str):
        """
        Cria um Usuario.

        Arguments:
            email {str}: Email do usuario.
            senha {str}: Senha do usuario.
        """
        self.email = email
        self.senha = senha
