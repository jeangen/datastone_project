from pydantic import BaseModel, validator

class ExchangeRateSchema(BaseModel):
    from_currency: str # Código da moeda de origem
    to_currency: str # Código da moeda de destino
    rate: float # Taxa de câmbio

    @validator('from_currency', 'to_currency')
    def currency_length(cls, value):
        if not (3 <= len(value) <= 3):
            raise ValueError("Currency code must be exactly 3 characters")
        return value

    @validator('rate')
    def positive_rate(cls, value):
        if value <= 0:
            raise ValueError("Rate must be greater than zero")
        return value

class ExchangeRateConversionSchema(BaseModel):
    from_currency: str # Código da moeda de origem
    to_currency: str # Código da moeda de destino
    rate: float # Taxa de câmbio
    converted_rate: float # Taxa de câmbio convertida


    @validator('from_currency', 'to_currency')
    def currency_length(cls, value):
        if not (3 <= len(value) <= 3):
            raise ValueError("Currency code must be exactly 3 characters")
        return value

    @validator('rate')
    def positive_rate(cls, value):
        if value <= 0:
            raise ValueError("Rate must be greater than zero")
        return value

    @validator('converted_rate')
    def positive_converted_rate(cls, value):
        if value < 0:
            raise ValueError("Converted rate must be greater than or equal to zero")
        return value
