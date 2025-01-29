from sqlalchemy import Column, Integer, String, Date, Enum
from config import db
import enum

class Tipos(enum.IntEnum):
    MOTOCICLETA = 1
    CARRO = 2
    UTILITARIO = 3
    CAMINHAO = 4
    OUTROS = 5

class Veiculo(db.Model):
    id = Column(Integer, primary_key=True)
    tipo = Column(Enum(Tipos), nullable=False)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50))
    renavam = Column(String(50), nullable=False, unique=True)
    placa = Column(String(10), nullable=False, unique=True)
    chassis = Column(String(50), nullable=False, unique=True)
    proprio = Column(Integer)
    licenciamento = Column(Date)
    ipva = Column(Date)
    observacao_carro = Column(String(255))

