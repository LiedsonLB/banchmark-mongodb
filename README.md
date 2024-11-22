# Benchmark MongoDB

Este projeto utiliza Docker para criar um ambiente isolado e Python para rodar o benchmark em um banco de dados MongoDB. Abaixo estão as instruções para configurar e executar o projeto em um container Docker com Ubuntu, configurar o ambiente virtual (venv), e rodar os testes.

# Como usar o Meu Benchmark

## Clone o repositório
```
git clone https://github.com/LiedsonLB/lb-banchmark-mongodb.git
```

## Build e Inicialize os serviços do container Docker em segundo plano
```
docker-compose up --build
```

## Execute o Terminal Linux
```
docker compose exec ubuntu-test bash
```

# Caso já tenha o Linux e o MongoDB em um servidor

## Clone o repositório
```
git clone https://github.com/usuario/seu-repositorio.git
```

## Entre no repositório
```
cd seu-repositorio
```

## instale o pacote necessário para criar ambientes virtuais Python
```
apt-get install python3-venv
python3 -m venv venv
```

## Ative seu ambiente de desenvolvimento
```
source venv/bin/activate
```

## Instale a biblioteca do pymongo
```
pip install pymongo
```

## Rode os testes
```
cd benchmark/
python benchmark.py
```