from sqlalchemy import DateTime
from flask_login import UserMixin

from models.Conexao import *
import bcrypt
class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nome = Column("nome", String(100), nullable=False)
    email = Column("email", String(100), nullable=False, unique=True)
    senha = Column("senha", String(120), nullable=False)
    funcao = Column("funcao", String(30), nullable=True)
    status = Column("status", String(3), nullable=True)
    dataContratacao = Column("data_contratacao", DateTime, nullable=True)
    urlFoto = Column("urlFoto", String(100), nullable=True)
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = bcrypt.hashpw(senha.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
Base.metadata.create_all(bind=engine)