from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base

# Cria uma instância de uma classe base para a declaração de modelos do SQLAlchemy
Base = declarative_base()

# Define uma classe de modelo para armazenar informações de taxas de câmbio no banco de dados
class ExchangeRate(Base):
    # Define o nome da tabela no banco de dados
    __tablename__ = "exchange_rates"

    # Define as colunas da tabela, incluindo um ID como chave primária
    id = Column(Integer, primary_key=True, index=True)
    from_currency = Column(String, index=True)
    to_currency = Column(String, index=True)
    rate = Column(Float)