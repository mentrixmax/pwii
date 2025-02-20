from sqlalchemy import DateTime

from models.Conexao import *

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nome = Column("nome", String(100), nullable=False)
    email = Column("email", String(100), nullable=False, unique=True)
    senha = Column("senha", String(10), nullable=False)
    funcao = Column("funcao", String(30), nullable=True)
    status = Column("status", String(3), nullable=True)
    dataContratacao = Column("data_contratacao", DateTime, nullable=True)
    urlFoto = Column("urlFoto", String(100), nullable=True)
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha
Base.metadata.create_all(bind=engine);