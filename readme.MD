# API de Conversão Monetária

Bem-vindo à API de Conversão Monetária! Esta API permite converter valores entre diferentes moedas, incluindo USD, BRL, EUR, BTC e ETH. Ela fornece cotações de moedas em tempo real.

## Como Usar

Para usar a API, você pode fazer requisições HTTP para os seguintes endpoints:

## Execução
Após clonar o projeto use os dois comandos para construir a imagem
```bash
cd datastone_project
docker build -t datastone-api .
docker run -p 8000:8000 datastone-api
```

É possível ver o enpoint acessando `http://0.0.0.0:8000/docs`

## Execução dos testes 
Após clonar o projeto use os dois comandos para construir a imagem
```bash
cd datastone_project
docker build -t datastone-api-tests -f Dockerfile.test .
docker run -it --rm datastone-api-tests
```
### Convertendo Moedas

Endpoint: `/convert_currency`

### Requisição e Retorno
- **Método**: POST
- **Corpo da Requisição (JSON)**:
  - `from_currency`: A moeda de origem (por exemplo, "USD").
  - `to_currency`: A moeda de destino (por exemplo, "BRL").
  - `rate`: O valor a ser convertido.

Exemplos de corpo da requisição e do retorno:
```json
{
    "from_currency": "USD",
    "to_currency": "BRL",
    "rate": 100
}

{
    "from_currency": "USD",
    "to_currency": "BRL",
    "rate": 100,
    "converted_rate": 550,
}
