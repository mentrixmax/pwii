from models.Conexao import *

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nome = Column("nome", String(100), nullable=False)
    email = Column("email", String(100), nullable=False, unique=True)
    senha = Column("senha", String(10), nullable=False)
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha
Base.metadata.create_all(bind=engine);