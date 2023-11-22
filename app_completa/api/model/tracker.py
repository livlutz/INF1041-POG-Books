from sqlalchemy import Column, Integer, Date, ForeignKey
from datetime import date

from  model import Base


class Tracker(Base):
    __tablename__ = 'tracker'

    data = Column("pk1_tracker", Date, default = date.today(), primary_key=True)
    usuario = Column("pk2_tracker", ForeignKey("usuario.email", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    qtd = Column(Integer, nullable=False)

    def __init__(self, data: date, usuario: str, qtd: int):
        """
        Cria um Registro de leitura

        Argumentos:
            data {date}: Data da leitura registrada
            usuario {str}: Email do usuario
            qtd {int}: Quantidade de páginas lidas
        """
        self.data = data
        self.usuario = usuario
        self.qtd = qtd
