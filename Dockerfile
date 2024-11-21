# Usar a imagem oficial do Ubuntu
FROM ubuntu:latest

# Atualizar os pacotes e instalar dependências necessárias
RUN apt-get update -y && \
    apt-get install -y git curl python3 python3-pip python3-venv && \
    apt-get clean

# Definir o diretório de trabalho para o projeto
WORKDIR /app

# Copiar os arquivos do projeto para dentro do contêiner
COPY . /app

# Instalar dependências do projeto usando requirements.txt (se existir)
RUN pip3 install --no-cache-dir -r requirements.txt

# Comando padrão para iniciar o contêiner
CMD ["/bin/bash"]