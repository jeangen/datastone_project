import requests
from bs4 import BeautifulSoup

# Define uma exceção personalizada para lidar com moedas inválidas
class InvalidCurrencyError(Exception):
    pass

# Classe que fornece informações de taxas de câmbio usando Google como fonte
class GoogleExchangeRateProvider:
    def __init__(self):
        self.base_url = "https://www.google.com/search?q="
    
    def fetch_exchange_rate(self, from_currency, to_currency):
        # Constrói a consulta para pesquisa no Google
        query = f"{from_currency} to {to_currency} exchange rate"
        url = self.base_url + query
        response = requests.get(url)
        
        # Envia uma solicitação GET para o Google
        if response.status_code == 200:
            # Analisa a resposta HTML usando BeautifulSoup
            return self.parse_exchange_rate(response.text)
        else:
            # Lança uma exceção em caso de falha na busca
            raise ConnectionError(f"Failed to fetch data from Google. Status code: {response.status_code}")

    @staticmethod
    def parse_exchange_rate(html):
        # Analisa o HTML para extrair a taxa de câmbio
        soup = BeautifulSoup(html, 'html.parser')

        try:
            exchange_rate = soup.find('div', {'class': 'BNeawe iBp4i AP7Wnd'}).text
            # Retorna a taxa de câmbio como um número de ponto flutuante
            return float(exchange_rate.split()[0].replace(",", "."))
        except Exception as e:
             # Lança uma exceção se a moeda for inválida ou a taxa de câmbio não for encontrada
            raise InvalidCurrencyError("Invalid currency or exchange rate not found.")

    def get_exchange_rate_info(self, from_currency, to_currency):
        try:
            # Obtém a taxa de câmbio entre as moedas especificadas
            rate = self.fetch_exchange_rate(from_currency, to_currency)
            # Retorna as informações da taxa de câmbio
            return {"from_currency": from_currency, "exchange_rate": rate, "to_currency": to_currency}
        except ConnectionError as e:
            # Retorna um erro em caso de falha na conexão com o Google
            return {'error': str(e)}
        except InvalidCurrencyError as e:
            # Retorna um erro se a moeda for inválida
            return {'error': str(e)}
