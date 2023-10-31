# API de Conversão Monetária

Bem-vindo à API de Conversão Monetária! Esta API permite converter valores entre diferentes moedas, incluindo USD, BRL, EUR, BTC e ETH. Ela fornece cotações de moedas em tempo real.

## Estrutura do Projeto
datastone_project/
│
├── app/
│   ├── __init__.py
│   ├── models.py 
│   ├── routes.py  
|   ├── schemas.py
|   ├── exchange_rate_provider.py
│   └── utils/
│       ├── __init__.py
│       ├── currency_conversion.py
│       ├── test_exchange_rate_provider.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│
├── tests/
│   ├── __init__.py
│   ├── test_routes.py
│
├── venv/
│
├── requirements.txt
│
├── run.py
│
└── .gitignore

## Como Usar

Para usar a API, você pode fazer requisições HTTP para os seguintes endpoints:

## Execução
Após clonar o projeto use os dois comandos para construir a imagem
cd datastone_project
docker build -t datastone-api .
docker run -p 8000:8000 datastone-api

## Execução dos testes 
Após clonar o projeto use os dois comandos para construir a imagem
cd datastone_project
docker build -t datastone-api-tests -f Dockerfile.test .
docker run -it --rm datastone-api-tests

### Convertendo Moedas

Endpoint: `/convert_currency`

#### Requisição e Retorno
- **Método**: POST
- **Corpo da Requisição (JSON)**:
  - `from_currency`: A moeda de origem (por exemplo, "USD").
  - `to_currency`: A moeda de destino (por exemplo, "BRL").
  - `rate`: O valor a ser convertido.

Exemplo de corpo da requisição:
```json
{
    "from_currency": "USD",
    "to_currency": "BRL",
    "rate": 100
}

- **Corpo do Retorno (JSON)**:
  - `from_currency`: A moeda de origem (por exemplo, "USD").
  - `to_currency`: A moeda de destino (por exemplo, "BRL").
  - `rate`: O valor a ser convertido.
  - `converted_rate`: O valor convertido.

Exemplo de corpo do retorno:
```json
{
    "from_currency": "USD",
    "to_currency": "BRL",
    "rate": 100,
    "converted_rate": 550
}
