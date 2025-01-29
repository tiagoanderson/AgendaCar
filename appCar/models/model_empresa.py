from sqlalchemy import Column, Integer, String, Date
from config import db




class Empresa(db.Model):
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    cnpj = Column(String(16), nullable=False, unique=True)
    cep = Column(String(11))
    rua = Column(String(50))
    numero = Column(String(10))
    bairro = Column(String(50))
    cidade = Column(String(50))
    estado = Column(String(50))
    email = Column(String(50), nullable=False)
    telefone = Column(String(50), nullable=False)
    observacao_pessoa = Column(String(255))
