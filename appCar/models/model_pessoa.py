from sqlalchemy import Column, Integer, String, Date
from config import db





class Pessoa(db.Model):
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    data_nascimento = Column(Date)
    cnh_categ = Column(String(15))
    cnh = Column(String(9), nullable=False, unique=True)
    data_vencimento_cnh = Column(Date)
    cep = Column(String(11))
    rua = Column(String(50))
    numero = Column(String(10))
    bairro = Column(String(50))
    cidade = Column(String(50))
    estado = Column(String(50))
    email = Column(String(50), nullable=False, unique=True)
    celular = Column(String(50), nullable=False, unique=True)
    observacao_pessoa = Column(String(255))
