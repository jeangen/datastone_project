# Use uma imagem oficial do Python como imagem pai
FROM python:3.8-slim

# Defina o diretório de trabalho para /app
WORKDIR /app

# Copie o conteúdo do diretório atual para o contêiner em /app
COPY . /app

# Instale os pacotes necessários especificados em requirements.txt
RUN pip install -r requirements.txt

# Disponibilize a porta 80 para o mundo exterior a partir deste contêiner
EXPOSE 80

# Defina variáveis de ambiente (se necessário)
ENV VARIABLE_NAME=value

# Crie um script para inicializar o banco de dados e depois iniciar a aplicação FastAPI
RUN echo '#!/bin/sh' > /start.sh && \
    echo 'python initialize_database.py' >> /start.sh && \
    echo 'uvicorn main:app --host 0.0.0.0 --port 8000' >> /start.sh && \
    chmod +x /start.sh

# Defina o comando CMD para executar o script
CMD ["/start.sh"]
