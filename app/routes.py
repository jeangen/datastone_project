from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import sessionmaker, Session
from app.models import ExchangeRate
from app.schemas import ExchangeRateSchema, ExchangeRateConversionSchema
from app.exchange_rate_provider import GoogleExchangeRateProvider
from config.settings import DATABASE_URL
from sqlalchemy import create_engine

# Inicializa o roteador do FastAPI
app = APIRouter()
# Cria uma conexão com o banco de dados usando a URL fornecida nas configurações
engine = create_engine(DATABASE_URL).connect()
# Define uma fábrica de sessões para o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Função para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Função para obter ou criar uma taxa de câmbio no banco de dados
def get_or_create_exchange_rate(db, from_currency, to_currency):
    # Verifica se a taxa de câmbio já existe no banco de dados
    exchange_rate = db.query(ExchangeRate).filter_by(from_currency=from_currency, to_currency=to_currency).first()
    
    # Se a taxa de câmbio não existir, tenta obter informações da taxa de câmbio de uma fonte externa (Google)
    if exchange_rate is None:
        provider = GoogleExchangeRateProvider()
        exchange_rate_info = provider.get_exchange_rate_info(from_currency, to_currency)
        
        # Verifica se há algum erro nas informações da taxa de câmbio
        if 'error' in exchange_rate_info.keys():
            raise HTTPException(status_code=400, detail=exchange_rate_info['error'])
        
        # Cria uma nova taxa de câmbio com as informações obtidas e a insere no banco de dados
        new_exchange_rate = ExchangeRate(
            from_currency=exchange_rate_info["from_currency"],
            to_currency=exchange_rate_info["to_currency"],
            rate=exchange_rate_info["exchange_rate"]
        )
        db.add(new_exchange_rate)
        db.commit()
        return new_exchange_rate
    # Se a taxa de câmbio já existir no banco de dados, retorna a taxa de câmbio existente    
    return exchange_rate

# Rota para realizar a conversão de moeda
@app.post("/convert_currency", response_model=ExchangeRateConversionSchema)
def currency_conversion(data: ExchangeRateSchema, db: Session = Depends(get_db)):
    from_currency = data.from_currency
    to_currency = data.to_currency
    rate = data.rate
    
    # Obtém ou cria a taxa de câmbio com base nas moedas de origem e destino
    exchange_rate = get_or_create_exchange_rate(db, from_currency, to_currency)
    
    # Calcula a taxa de câmbio convertida
    converted_rate = exchange_rate.rate * rate
    
    # Cria a resposta com as informações de conversão
    response = ExchangeRateConversionSchema(
            from_currency=from_currency,
            to_currency=to_currency,
            rate=rate,
            converted_rate=converted_rate
        )
    return response