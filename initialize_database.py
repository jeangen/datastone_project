from sqlalchemy import inspect, create_engine, MetaData, Table, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from app.models import ExchangeRate
from config.settings import DATABASE_URL
from sqlalchemy.orm.exc import NoResultFound

# Dados de exemplo das taxas de câmbio
exchange_rates_data = {
    "USD": {
        "BRL": 5.50,
        "EUR": 0.85,
        "BTC": 0.000022,
        "ETH": 0.00032
    },
    "BRL": {
        "USD": 0.18,
        "EUR": 0.15,
        "BTC": 0.000004,
        "ETH": 0.00006
    },
    "EUR": {
        "USD": 1.18,
        "BRL": 6.72,
        "BTC": 0.000026,
        "ETH": 0.00038
    },
    "BTC": {
        "USD": 45517.0,
        "BRL": 227585.0,
        "EUR": 37917.0,
        "ETH": 14.0
    },
    "ETH": {
        "USD": 3126.0,
        "BRL": 15630.0,
        "EUR": 2605.0,
        "BTC": 0.071
    }
}

# Inicializa o banco de dados
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData()

exchange_rate_table = Table(
    'exchange_rates',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('from_currency', String, index=True),
    Column('to_currency', String, index=True),
    Column('rate', Float),
)

if not inspect(engine).has_table(engine, 'exchange_rates'):
    metadata.create_all(engine)

# Cria registros de taxa de câmbio no banco de dados
def populate_exchange_rates():
    db = SessionLocal()
    try:
        for from_currency, rates in exchange_rates_data.items():
            for to_currency, rate in rates.items():
                try:
                    existing_rate = (
                        db.query(ExchangeRate)
                        .filter_by(from_currency=from_currency, to_currency=to_currency)
                        .one()
                    )
                    existing_rate.rate = float(rate)
                except NoResultFound:
                    exchange_rate = ExchangeRate(
                        from_currency=from_currency,
                        to_currency=to_currency,
                        rate=float(rate))
                    db.add(exchange_rate)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    populate_exchange_rates()